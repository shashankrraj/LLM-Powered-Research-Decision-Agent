from fastapi import FastAPI
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    question: str
    context: str | None = None


class MemoSection(BaseModel):
    title: str
    content: str


class DecisionMemo(BaseModel):
    question: str
    sections: list[MemoSection]
    recommendation: str


app = FastAPI(title="LLM-Powered Research & Decision Agent")


@app.get("/")
async def root():
    return {"message": "Decision Agent backend is running"}


@app.post("/analyze", response_model=DecisionMemo)
async def analyze(req: AnalyzeRequest) -> DecisionMemo:
    """Stub endpoint: returns a hard-coded memo until the OpenClaw agent is wired in.

    Later this function will:
    - call the OpenClaw agent with the question + context
    - use local LLM (DeepSeek/Qwen) + tools to build a real memo
    """
    sections = [
        MemoSection(
            title="Summary",
            content=(
                "This is a placeholder decision memo. The agent pipeline "
                "(OpenClaw + local LLM + tools) is not wired in yet."
            ),
        ),
        MemoSection(
            title="Next steps",
            content=(
                "1) Implement agent call in this endpoint.\n"
                "2) Add web + knowledge base tools.\n"
                "3) Refine memo structure based on real outputs."
            ),
        ),
    ]
    return DecisionMemo(
        question=req.question,
        sections=sections,
        recommendation="Further analysis required (pipeline not yet connected).",
    )
