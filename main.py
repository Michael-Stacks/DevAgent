
from utils.rag_utils import build_or_load_vector_db, retrieve_context
from utils.patch_utils import generate_patch
from utils.sandbox_utils import apply_patch, run_in_sandbox
import sys, json, subprocess

def main(instruction):
    print(f"Instruction: {instruction}")
    db = build_or_load_vector_db(".")
    results = retrieve_context(db, instruction, k=3)
    context = "\n".join([r.page_content for r in results])
    patch_text = generate_patch(instruction, context)
    print("Patch proposed:\n", patch_text[:400])
    apply_patch(patch_text)
    result = run_in_sandbox()
    summary = result.get("report", {}).get("summary", {})
    print("=== TEST SUMMARY ===")
    print(json.dumps(summary, indent=2))
    if summary.get("failed", 1) == 0:
        print("✅ All tests passed. Patch accepted!")
    else:
        print("❌ Tests failed. Patch reverted.")
        subprocess.run(["git", "reset", "--hard"], check=False)

if __name__ == "__main__":
    main("Fix add() to handle string inputs properly")
