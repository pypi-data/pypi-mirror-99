import binascii
import logging
import os
import pickle
import sqlite3
import sys
from collections import defaultdict
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy import event
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import (
    mapper,
    relationship,
)
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.orm.exc import NoResultFound  # noqa
from sqlalchemy.sql import sqltypes as st
from starlette.exceptions import HTTPException

from otree import __version__
from otree import common
from otree import settings
from otree.common import expand_choice_tuples, get_models_module
from otree.currency import Currency, RealWorldCurrency

logger = logging.getLogger(__name__)
DB_FILE = 'db.sqlite3'


# DB_FILE_PATH = Path(DB_FILE)


def get_disk_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def get_mem_conn():
    return sqlite3.connect(':memory:', check_same_thread=False)


def get_schema(conn):
    conn.text_factory = str
    cur = conn.cursor()

    result = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    table_names = sorted(list(zip(*result))[0])

    d = {}
    for table_name in table_names:
        result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
        d[table_name] = list(zip(*result))[1]
    return d


NEW_IDMAP_EACH_REQUEST = True

sqlite_mem_conn = get_mem_conn()
sqlite_disk_conn = get_disk_conn()

_dumped = False


class OTreeColumn(sqlalchemy.Column):
    form_props: dict
    auto_submit_default = None


def load_in_memory_db():
    old_schema = get_schema(sqlite_disk_conn)
    new_schema = get_schema(sqlite_mem_conn)

    disk_cur = sqlite_disk_conn.cursor()
    mem_cur = sqlite_mem_conn.cursor()

    prev_version = sqlite_disk_conn.execute("PRAGMA user_version").fetchone()[0]

    # They should start fresh so that:
    # (1) performance refresh
    # (2) don't have to worry about old references to things that were removed from otree-core.
    if prev_version != version_for_pragma() and not os.getenv('OTREE_CORE_DEV'):
        sys.exit(f'oTree has been updated. Please delete your database ({DB_FILE})')

    for tblname in new_schema:
        if tblname in old_schema:
            common_cols = [c for c in old_schema[tblname] if c in new_schema[tblname]]
            common_cols_joined = ', '.join(common_cols)
            select_cmd = f'SELECT {common_cols_joined} FROM {tblname}'
            question_marks = ', '.join('?' for _ in common_cols)
            insert_cmd = (
                f'INSERT INTO {tblname}({common_cols_joined}) VALUES ({question_marks})'
            )
            disk_cur.execute(select_cmd)
            rows = disk_cur.fetchall()
            mem_cur.executemany(insert_cmd, rows)
    sqlite_mem_conn.commit()


@contextmanager
def session_scope():
    if NEW_IDMAP_EACH_REQUEST:
        db.new_session()
    try:
        yield
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        if NEW_IDMAP_EACH_REQUEST:
            db.close()


def save_sqlite_db():
    global _dumped
    if _dumped:
        return
    sqlite_mem_conn.cursor().execute(f"PRAGMA user_version = {version_for_pragma()}")
    sqlite_mem_conn.backup(sqlite_disk_conn)
    _dumped = True


DeclarativeBase = declarative_base()


class DBWrapper:
    """
    1. this way we can defer definining the ._db attribute
    until all modules are imported
    2. we can add helper methods
    """

    _db: sqlalchemy.orm.Session = None

    def query(self, *args, **kwargs):
        return self._db.query(*args, **kwargs)

    def add(self, obj):
        return self._db.add(obj)

    def add_all(self, objs):
        return self._db.add_all(objs)

    def delete(self, obj):
        return self._db.delete(obj)

    def get_or_404(self, Model, msg='Not found', **kwargs):
        try:
            return self.query(Model).filter_by(**kwargs).one()
        except sqlalchemy.orm.exc.NoResultFound:
            msg = f'{msg}: {Model.__name__}, {kwargs}'
            raise HTTPException(404, msg)

    def commit(self):
        try:
            return self._db.commit()
        except:
            self._db.rollback()
            raise

    def rollback(self):
        return self._db.rollback()

    def close(self):
        return self._db.close()

    def new_session(self):
        if os.getenv('OTREE_EPHEMERAL'):
            self._db = DBSession(bind=ephemeral_connection)
        else:
            self._db = DBSession()

    def expire_all(self):
        self._db.expire_all()


db = DBWrapper()
dbq = db.query

# is_test = 'test' in sys.argv
# # is_devserver = 'devserver_inner' in sys.argv
# # is_devserver = False  ## FIXME: dont use in memory DB for now
# is_devserver = True


IN_MEMORY = bool(os.getenv('OTREE_IN_MEMORY'))


def get_engine():
    if IN_MEMORY:
        engine = create_engine(
            'sqlite://',
            creator=lambda: sqlite_mem_conn,
            # with NullPool i get 'cannot
            poolclass=sqlalchemy.pool.StaticPool,
        )
    else:
        DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DB_FILE}')
        kwargs = {}
        if DATABASE_URL.startswith('sqlite'):
            kwargs['creator'] = lambda: sqlite_disk_conn
        engine = create_engine(
            DATABASE_URL, poolclass=sqlalchemy.pool.StaticPool, **kwargs,
        )
    return engine


engine = get_engine()

DBSession = sessionmaker(bind=engine)

ephemeral_connection = None


class VarsDescriptor:
    def __init__(self, attr):
        self.attr = attr

    def __get__(self, obj, objtype=None):
        return obj.vars[self.attr]

    def __set__(self, obj, value):
        obj.vars[self.attr] = value


def init_orm():
    from otree.settings import OTREE_APPS

    # import all models so it's loaded into the engine?
    for app in OTREE_APPS:
        if len(app) > 45:
            msg = f'App name is too long: {app}'
            sys.exit(msg)
        try:
            models = get_models_module(app)
        except Exception as exc:
            # to produce a smaller traceback
            import traceback

            traceback.print_exc()
            sys.exit(1)

        if not hasattr(models, 'Player'):
            if Path(app, 'app.py').exists():
                sys.exit(
                    'app.py has been replaced by __init__.py. run "otree remove_self" again'
                )

        # make get_FIELD_display

        is_noself = common.is_noself(app)
        for cls in [models.Player, models.Group, models.Subsession]:
            cls._is_frozen = False
            cls.is_noself = is_noself
            # don't set _is_frozen back because this is just on startup

            target = cls.get_user_defined_target()
            for field in cls.__table__.columns:
                if isinstance(field, OTreeColumn):
                    name = field.name
                    if hasattr(target, name + '_choices'):
                        method = make_get_display_dynamic(name)
                    elif field.form_props.get('choices'):
                        method = make_get_display_static(
                            name, field.form_props['choices']
                        )
                    else:
                        method = None
                    if method:
                        method_name = f'get_{name}_display'
                        setattr(cls, method_name, method)
            cls.freeze_setattr()
    from otree.models import Participant, Session

    for cls, setting_name in [
        (Session, 'SESSION_FIELDS'),
        (Participant, 'PARTICIPANT_FIELDS'),
    ]:
        for attr in getattr(settings, setting_name):
            if hasattr(cls, attr):
                msg = f'{setting_name} cannot contain "{attr}" because that name is reserved.'
                sys.exit(msg)
            setattr(cls, attr, VarsDescriptor(attr))
        cls.freeze_setattr()

    # just ensure it gets created
    import otree.models_concrete  # noqa

    configure_mappers()
    AnyModel.metadata.create_all(engine)

    if (
        IN_MEMORY
        and not os.getenv('OTREE_EPHEMERAL')
        and Path(DB_FILE).exists()
        and Path(DB_FILE).stat().st_size > 0
    ):
        load_in_memory_db()

    db.new_session()


class AnyModel(DeclarativeBase):
    __abstract__ = True

    id = Column(st.Integer, primary_key=True)

    def __repr__(self):
        return '<{} id={}>'.format(self.__class__.__name__, self.id)

    @declared_attr
    def __tablename__(cls):
        return cls.get_folder_name() + '_' + cls.__name__.lower()

    @classmethod
    def get_folder_name(cls):
        """this works for models.py format and no-self format"""
        for part in reversed(cls.__module__.split('.')):
            if part != 'models':
                return part

    def _clone(self):
        return type(self).objects_get(id=self.id)

    @classmethod
    def objects_get(cls, *args, **kwargs) -> 'AnyModel':
        try:
            return cls.objects_filter(*args, **kwargs).one()
        except Exception as exc:
            raise

    @classmethod
    def objects_first(cls, *args, **kwargs) -> 'AnyModel':
        return cls.objects_filter(*args, **kwargs).first()

    @classmethod
    def objects_filter(cls, *args, **kwargs):
        return dbq(cls).filter(*args).filter_by(**kwargs)

    @classmethod
    def objects_exists(cls, *args, **kwargs) -> bool:
        return bool(cls.objects_filter(*args, **kwargs).first())

    @classmethod
    def values_dicts(cls, *args, order_by=None, **kwargs):
        query = cls.objects_filter(*args, **kwargs)
        if order_by:
            query = query.order_by(order_by)
        names = [f.name for f in cls.__table__.columns]
        fields = [getattr(cls, name) for name in names]
        # i if I use .values(), I get 'no such column: id'
        return [dict(zip(names, row)) for row in query.with_entities(*fields)]

    @classmethod
    def objects_create(cls, **kwargs) -> 'AnyModel':
        obj = cls(**kwargs)
        db.add(obj)
        return obj

    @classmethod
    def freeze_setattr(cls):
        cls._setattr_fields = frozenset(f.name for f in cls.__table__.columns)
        cls._setattr_attributes = frozenset(dir(cls))


class BaseCurrencyType(types.TypeDecorator):
    impl = types.Text()

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(Decimal(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.MONEY_CLASS(Decimal(value))

    MONEY_CLASS = None  # need to set in subclasses


class CurrencyType(BaseCurrencyType):
    MONEY_CLASS = Currency


class RealWorldCurrencyType(BaseCurrencyType):
    MONEY_CLASS = RealWorldCurrency


class MRU:
    def __init__(self):
        self._d = defaultdict(int)
        self._count = 0

    def add(self, item):
        if (
            item.startswith('_')
            or item.endswith('_id')
            or item in ['id', 'group', 'subsession', 'session', 'participant',]
        ):
            return
        # make it a bit bigger than we need because we will need to throw out methods
        self._count += 1
        self._d[item] = self._count

    def most_recent(self):
        return [
            attr
            for attr, count in sorted(
                self._d.items(), key=lambda ele: ele[1], reverse=True
            )
        ]


mru_dict = defaultdict(MRU)


class SSPPGModel(AnyModel):
    __abstract__ = True

    _is_frozen = False

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        # nonexistent fields can be set in creating_session because the Participant
        # was just created, and init_on_load did not get run yet.
        # but that's OK because anywhere else, users will be told.
        self._is_frozen = True

    NoneType = type(None)

    _setattr_datatypes = {
        # first value should be the "recommmended" datatype,
        # because that's what we recommend in the error message.
        # it seems the habit of setting boolean values to 0 or 1
        # is very common. that's even what oTree shows in the "live update"
        # view, and the data export.
        st.Boolean: (bool, int, NoneType),
        # forms seem to save Decimal to CurrencyField
        CurrencyType: (Currency, NoneType, int, float, Decimal),
        st.Float: (float, NoneType, int),
        st.Integer: (int, NoneType),
        st.String: (str, NoneType),
        st.Text: (str, NoneType),
    }
    _setattr_whitelist = {
        '_is_frozen',
    }

    def __setattr__(self, field_name: str, value):
        if self._is_frozen and hasattr(self, '_setattr_fields'):

            if field_name in self._setattr_fields:
                # hasattr() cannot be used inside
                # a Django model's setattr, as I discovered.
                field = self.__table__.columns[field_name]

                field_type_name = type(field.type)

                if field_type_name in self._setattr_datatypes:
                    allowed_types = self._setattr_datatypes[field_type_name]
                    if (
                        isinstance(value, allowed_types)
                        # numpy uses its own datatypes, e.g. numpy._bool,
                        # which doesn't inherit from python bool.
                        or 'numpy' in str(type(value))
                    ):
                        pass
                    else:
                        msg = ('{} should be set to {}, not {}.').format(
                            field_name, allowed_types[0].__name__, type(value).__name__,
                        )
                        raise TypeError(msg)
            elif (
                field_name in self._setattr_attributes
                or field_name in self._setattr_whitelist
            ):
                pass
            else:
                msg = ('{} has no field "{}".').format(
                    self.__class__.__name__, field_name
                ) + self._SETATTR_NO_FIELD_HINT
                raise AttributeError(msg)
            mru_dict[type(self)].add(field_name)
            super().__setattr__(field_name, value)
        else:
            # super() is a bit slower but only gets run during __init__
            super().__setattr__(field_name, value)

    _SETATTR_NO_FIELD_HINT = ''


class NullFieldError(TypeError):
    pass


class SPGModel(SSPPGModel):
    __abstract__ = True
    is_noself = True

    def __getattribute__(self, attr):

        # we add to mru dict only on getattr, not on setattr, because a field cannot cause a
        # failure until it is actually accessed. on the error page when we show local vars,
        # we want to show the recently accessed attributes.
        # also, setattr is already defined at the SSPPG level, and we don't want to override it.
        mru_dict[type(self)].add(attr)
        res = super().__getattribute__(attr)
        if res is None and super().__getattribute__('_is_frozen'):
            object_name = self.__class__.__name__.lower()
            # 2 ways for users to work around this:
            # - set the initial value to something other than None
            # - catch the TypeError
            msg = (
                f'{object_name}.{attr} is None. '
                f'Accessing a null field is generally considered an error. '
            )
            raise TypeError(msg)
        return res

    def __repr__(self):
        cls = type(self)
        colnames = [f.name for f in cls.__table__.columns]
        items = []
        # reverse it so that we don't modify the MRU
        for attr in reversed(mru_dict[cls].most_recent()):
            if attr in colnames:
                try:
                    v = repr(getattr(self, attr))
                except TypeError:
                    v = 'None'
                if len(v) > 15:
                    v = v[:15] + '...'
                items.append((attr, v))
                if len(items) >= 5:
                    break
        attr_string = ', '.join(reversed(list(f'{k}={v}' for k, v in items)))
        return f'{cls.__name__}({attr_string})'

    def call_user_defined(self, funcname, *args, missing_ok=False, **kwargs):
        target = self.get_user_defined_target()
        func = getattr(target, funcname, None)
        if func is None and missing_ok:
            return
        return func(self, *args, **kwargs)

    @classmethod
    def get_user_defined_target(cls):
        if cls.is_noself:
            app_name = cls.get_folder_name()
            return get_models_module(app_name)
        return cls

    def get_field_display(self, name):
        value = getattr(self, name)
        target = self.get_user_defined_target()
        choices_func = getattr(target, name + '_choices', None)
        if choices_func:
            choices = choices_func(self)
        else:
            choices = getattr(type(self), name).form_props['choices']
        return dict(expand_choice_tuples(choices))[value]


class UndefinedUserFunction(Exception):
    pass


class MixinSessionFK:
    """can this be combined with SPGModel? maybe there was a specific reason it needed
    to be a mixin."""

    @declared_attr
    def session_id(cls):
        return Column(st.Integer, ForeignKey(f'otree_session.id'))

    @declared_attr
    def session(cls):
        # just some random name
        backref_name = f'{cls.get_folder_name()}_{cls.__name__}'
        # backref needed to ensure all objects are deleted with the session.
        return relationship(
            f'Session',
            backref=sqlalchemy.orm.backref(backref_name, cascade="all, delete-orphan"),
        )


class VarsError(Exception):
    pass


def values_flat(query, field) -> list:
    return [val for [val] in query.with_entities(field)]


def inspect_obj(obj):
    if isinstance(obj, AnyModel):
        msg = (
            "Cannot store '{}' object in vars. "
            "participant.vars and session.vars "
            "cannot contain model instances, "
            "like Players, Groups, etc.".format(repr(obj))
        )
        raise VarsError(msg)


def scan_for_model_instances(vars_dict: dict):
    '''
    I don't know how to entirely block pickle from storing model instances,
    (I tried overriding __reduce__ but that interferes with deepcopy())
    so this simple shallow scan should be good enough.
    '''

    for v in vars_dict.values():
        inspect_obj(v)
        if isinstance(v, dict):
            for vv in v.values():
                inspect_obj(vv)
        elif isinstance(v, list):
            for ele in v:
                inspect_obj(ele)


def make_get_display_static(name, choices):
    def get_FIELD_display(self):
        value = getattr(self, name)
        return dict(expand_choice_tuples(choices))[value]

    return get_FIELD_display


def make_get_display_dynamic(name):
    def get_FIELD_display(self):
        target = self.get_user_defined_target()
        choices = getattr(target, name + '_choices')(self)
        value = getattr(self, name)
        return dict(expand_choice_tuples(choices))[value]

    return get_FIELD_display


class VarsDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, VarsDict):
            if isinstance(value, dict):
                return VarsDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value


class _PickleField(types.TypeDecorator):
    impl = types.Text

    def process_bind_param(self, value, dialect):
        # for some reason this doesn't print the actual VarsError, but rather
        # a really ugly sqlalchemy.exc.StatementError.
        # scan_for_model_instances(value)
        return binascii.b2a_base64(pickle.dumps(dict(value))).decode('utf-8')

    def process_result_value(self, value, dialect):
        return pickle.loads(binascii.a2b_base64(value.encode('utf-8')))


class MixinVars:
    _vars = Column(VarsDict.as_mutable(_PickleField), default=VarsDict)

    @property
    def vars(self):
        self._vars.changed()
        return self._vars


AUTO_SUBMIT_DEFAULTS = {
    st.Boolean: False,
    st.Integer: 0,
    st.Float: 0,
    st.String: '',
    st.Text: '',
    RealWorldCurrencyType: Currency(0),
    CurrencyType: RealWorldCurrency(0),
}


def wrap_column(coltype, *, initial=None, null=True, **form_props) -> OTreeColumn:
    if 'default' in form_props:
        initial = form_props.pop('default')

    col = OTreeColumn(coltype, default=initial, nullable=null)
    col.form_props = form_props

    col.auto_submit_default = AUTO_SUBMIT_DEFAULTS[
        coltype if isinstance(coltype, type) else type(coltype)
    ]
    return col


def BooleanField(**kwargs):
    return wrap_column(st.Boolean, **kwargs)


def StringField(**kwargs):
    return wrap_column(st.String(length=kwargs.get('max_length', 10000)), **kwargs,)


def LongStringField(**kwargs):
    return wrap_column(st.Text, **kwargs)


def FloatField(**kwargs):
    return wrap_column(st.Float, **kwargs)


def IntegerField(**kwargs):
    return wrap_column(st.Integer, **kwargs)


def CurrencyField(**kwargs):
    return wrap_column(CurrencyType, **kwargs)


def RealWorldCurrencyField(**kwargs):
    return wrap_column(RealWorldCurrencyType, **kwargs)


# aliases for compat
CharField = StringField
PositiveIntegerField = IntegerField
TextField = LongStringField


def get_changed_columns(old_schema, new_schema):
    return dict(
        dropped_tables=None, new_tables=None, dropped_columns=None, new_columns=None
    )


def version_for_pragma() -> int:
    # e.g. '3.0.25b1' -> 3025
    # not perfect but as long as it works 95% of the time it's good enough
    return int(''.join(c for c in __version__ if c in '0123456789'))


class Link:
    """A class attribute that generates a mapped attribute
    after mappers are configured."""

    def __init__(self, target_cls):
        self.target_cls = target_cls

    def _config(self, cls, key):
        target_cls = self.target_cls
        pk_table = target_cls.__table__
        pk_col = list(pk_table.primary_key)[0]

        fk_colname = f'{key}_id'

        # zzeeek's example passed the string name as first arg
        fk_col = Column(fk_colname, pk_col.type, ForeignKey(pk_col))
        setattr(cls, fk_colname, fk_col)

        rel = relationship(
            target_cls, primaryjoin=fk_col == pk_col, collection_class=set,
        )
        setattr(cls, key, rel)


class ExtraModel(AnyModel):
    __abstract__ = True

    @classmethod
    def filter(cls, **kwargs):
        # prevent people from absent-minded queries like Bid.filter(amount=10)
        # that forgot to filter to the current session.
        # this allows querying .filter() without any args for custom_export,
        # but not in normal circumstances.
        if kwargs and not any(isinstance(v, AnyModel) for v in kwargs.values()):
            raise ValueError(
                "At least one argument to .filter() must be a model instance, e.g. player=player or group=group"
            )
        return list(cls.objects_filter(**kwargs).order_by('id'))

    @classmethod
    def create(cls, **kwargs):
        # we could automatically convert the type here, but maybe not worth
        # the hassle, since we also need to think about None, empty string, etc.
        obj = cls(**kwargs)
        db.add(obj)
        return obj

    def delete(self):
        db.delete(self)

    def __repr__(self):
        cls = type(self)
        items = []
        # a bit more complex to get all foreign keys, in case we want to
        # show which player it relates to.
        for col in cls.__table__.columns:
            name = col.name
            if not (col.primary_key or col.foreign_keys):
                items.append((name, repr(getattr(self, name))))
        attr_string = ', '.join(list(f'{k}={v}' for k, v in items))
        return f'{cls.__name__}({attr_string})'


@event.listens_for(mapper, "instrument_class")
def prevent_forbidden_colnames(mapper, cls):
    if not cls.id.primary_key:
        sys.exit(
            f'"id" cannot be used as a field name on model {cls.__name__} because this name is reserved'
        )


@event.listens_for(mapper, "mapper_configured")
def _setup_deferred_properties(mapper, class_):
    """Listen for finished mappers and apply DeferredProp
    configurations."""

    for key, value in list(class_.__dict__.items()):
        if isinstance(value, Link):
            value._config(class_, key)
