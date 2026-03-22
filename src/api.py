from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .scraper import search_youtube
from .formatter import format_video_data

app = FastAPI(title="VideoRank API")

# CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "VideoRank API is running"}


@app.get("/search")
def search(
    query: str = Query(..., min_length=2),
    mode: str = Query("best"),
    max_results: int = Query(10, ge=1, le=50),
    min_views: int = Query(10000, ge=0)
):
    try:
        raw_data = search_youtube(query, max_results)

        if not raw_data:
            raise HTTPException(status_code=404, detail="No results found")

        # BEST MODE (default)
        if mode == "best":
            results = format_video_data(raw_data, query, min_views)

        # TRENDING MODE (sort by views only)
        elif mode == "trending":
            results = format_video_data(raw_data, query, 0)
            results.sort(key=lambda x: x["views"], reverse=True)

        # OPPORTUNITY MODE (low views + high relevance)
        elif mode == "opportunity":
            results = format_video_data(raw_data, query, 0)
            results = [v for v in results if v["views"] < 500000]
            results.sort(key=lambda x: x["score"], reverse=True)

        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

        return {
            "query": query,
            "mode": mode,
            "total_fetched": len(raw_data),
            "results_count": len(results),
            "results": results
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))