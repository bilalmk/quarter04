from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("Mcp server")


class Weather(BaseModel):
    message: str


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures",
    "outlook.pdf": "This document presents the projected future performance of the system",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(doc_id: str = Field(description="Id of the document to read")):
    return docs[doc_id]


@mcp.resource(uri="docs://document", mime_type="application/json")
def get_document_list():
    return list[docs.keys()]


@mcp.resource(uri="docs://document/{doc_id}", mime_type="application/json")
def get_document(doc_id: str):
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(doc_id: str) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [base.UserMessage(prompt)]


# mcp_server = mcp.streamable_http_app

if __name__ == "__main__":
    mcp.run()
