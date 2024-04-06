#!/bin/bash
uvicorn server.app.__init__:connex_app --reload
