import logging
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# [수정] 상대 경로 점(.)을 제거하여 어디서 실행하든 에러가 안 나게 변경
try:
    from algorithms import run_all_sorts
except ImportError:
    from .algorithms import run_all_sorts
