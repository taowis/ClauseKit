import os
import pytest
from langchain.docstore.document import Document
from rag import retriever


def test_load_knowledge_base(tmp_path):
    """
    Test full knowledge base loading using temporary FAISS store.
    Ensures no dependence on local files.
    """
    # Arrange: Create dummy documents and build FAISS store
    dummy_docs = [Document(page_content="This is a rental agreement between landlord and tenant.")]
    retriever.build_vector_store(dummy_docs, persist_path=str(tmp_path))

    # Act: Load the retriever and QA chain
    qa_chain = retriever.load_knowledge_base(persist_path=str(tmp_path))

    # Assert: QA chain is initialized correctly
    assert qa_chain is not None
    assert hasattr(qa_chain, "run")


def test_qa_chain_response(tmp_path):
    """
    Test running a query through the QA chain with mock documents.
    """
    dummy_docs = [Document(page_content="The landlord can terminate the lease under certain conditions.")]
    retriever.build_vector_store(dummy_docs, persist_path=str(tmp_path))

    chain = retriever.load_knowledge_base(persist_path=str(tmp_path))
    result = chain.run("Can the landlord terminate the lease early?")

    assert isinstance(result, str)
    assert len(result) > 0