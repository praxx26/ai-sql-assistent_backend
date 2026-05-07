from fastapi import FastAPI
from models.request_model import QueryRequest
from database.connection import create_connection
from database.schemareader import get_schema
from ai.ai_engine import generate_sql,generate_study_sql
from database.executer import execute_query
from ai.explain_sql import explain_sql
from models.study_model import StudyQueryRequest
import time

from history.study_history import (
    save_study_history,
    get_study_history,
    delete_study_history
)

from history.execute_history import (
    save_execute_history,
    get_execute_history,
    delete_execute_history
)

app = FastAPI()


@app.post("/generate-and-execute")
def generate_query(
    request: QueryRequest,
    limit: int = 10,
    page: int = 1
):

    try:

        conn = create_connection(
            host=request.host,
            port=request.port,
            user=request.user,
            password=request.password.get_secret_value(),
            database=request.database
        )

        schema = get_schema(conn)
        sql_query = generate_sql(schema, request.question)
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        for keyword in dangerous_keywords:
            if keyword in sql_query.upper():
                return {
                    "error": f"{keyword} queries are not allowed"
                }
        offset = (page - 1) * limit
        sql_query += f" LIMIT {limit} OFFSET {offset}"
        start_time = time.time()
        results = execute_query(conn, sql_query)
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        explanation = explain_sql(sql_query)
        explanation = explanation.replace('"', '')
        clean_sql = " ".join(sql_query.split())

        save_execute_history(
            request.database,
            request.question,
            clean_sql,
            explanation,
            results
        )

        return {
            "question": request.question,
            "sql_query": clean_sql,
            "explanation": explanation,
            "results": results,
            "page": page,
            "limit": limit,
            "execution_time_seconds": execution_time
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/study-sql")
def study_sql(request: StudyQueryRequest):

    try:
        sql_query = generate_study_sql(request.question)
        explanation = explain_sql(sql_query)
        explanation = explanation.replace('"', '')
        clean_sql = " ".join(sql_query.split())
        save_study_history(
            request.question,
            clean_sql,
            explanation
        )
        return {
            "question":request.question,
            "sql_query":clean_sql,
            "explanation":explanation
        }

    except Exception as e:

        return {
            "error":str(e)
        }


@app.get("/study-history")
def study_history_api():
    history = get_study_history()
    return {
        "total": len(history),
        "history": history
    }


@app.get("/execute-history")
def execute_history_api():
    history = get_execute_history()
    return {
        "total": len(history),
        "history": history
    }


@app.delete("/delete-study-history")
def delete_study_history_api():
    delete_study_history()
    return {
        "message": "Study history deleted successfully"
    }


@app.delete("/delete-execute-history")
def delete_execute_history_api():
    delete_execute_history()
    return {
        "message": "Execute history deleted successfully"
    }