import os

import pandas as pd

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from sqlalchemy import create_engine

from parser import run_parser_sync

load_dotenv()

app = FastAPI()

@app.get('/parse')
def start_parsing(
    styles: str = Query("y2k", description="Styles, example: y2k,grunge"),
    tags: str = Query("outfit", description="Tags, example: outfit,accessories"),
    max_pins: int = Query(10, description="Max pins"),
    scrolls: int = Query(5, description="Count scrolls")
):
    styles_list = [s.strip() for s in styles.split(',')]
    tags_list = [t.strip() for t in tags.split(',')]
    
    state_path = os.path.join(os.path.dirname(__file__), "state.json")

    try:
        run_parser_sync(
            state_path=state_path,
            styles=styles_list,
            tags=tags_list,
            max_pins=max_pins,
            scrolls=scrolls
        )
        
        return {
            "status": "success",
            "message": f"End!!!",
            "params": {
                "styles": styles_list,
                "tags": tags_list,
                "max_pins": max_pins,
                "scrolls": scrolls
            }
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
@app.get('/get_data')
def get_data():
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        
        query = "SELECT * FROM pins"
        df = pd.read_sql(query, con=engine)

        df = df.fillna('')
        
        return {
            "count": len(df),
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}