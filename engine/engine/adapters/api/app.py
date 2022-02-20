import logging
from os import environ, path
from typing import Any, Dict, Optional

import attr
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import dependencies, views

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class AppConfig:
    DB_URL: str


def get_config() -> AppConfig:
    if "ENGINE_CONFIG_DIR" not in environ:
        raise RuntimeError("no ENGINE_CONFIG_DIR set!")

    config_path = path.join(environ["ENGINE_CONFIG_DIR"], "engine_config.yaml")
    if not path.isfile(config_path):
        msg = "config file {} does not exist".format(config_path)
        logging.critical(msg)
        raise RuntimeError(msg)

    with open(config_path) as config_f:
        config_dict = yaml.safe_load(config_f)

    return AppConfig(DB_URL=config_dict["DB_URL"])


def setup_app(
    app: FastAPI,
    dependency_overrides: Optional[Dict[Any, Any]] = None,
) -> FastAPI:

    if dependency_overrides:
        for key, value in dependency_overrides.items():
            app.dependency_overrides[key] = value

    return app


def create_app(config: Optional[AppConfig] = None) -> FastAPI:
    app = FastAPI()

    config = config or get_config()

    session_cls = sessionmaker(
        bind=create_engine(config.DB_URL), autoflush=False
    )

    app = setup_app(
        app,
        dependency_overrides={
            dependencies.session_cls: lambda: session_cls,
        },
    )

    app.include_router(views.v1, prefix="/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
