import json
import sqlite3
import os

DB_PATH = "data/pulse.db"
BOARD_ID = "af285ee4-9a28-4369-bc9a-ac5ab7c75c7b"
OUTPUT_DIR = "docs/reference-run"

def export_table(conn, query, params, output_filename):
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
        
    out_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(data)} rows to {out_path}")

def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    try:
        # 1. board.json
        export_table(conn, "SELECT * FROM boards WHERE id = ?", (BOARD_ID,), "board.json")
        
        # 2. activity_logs.json
        export_table(conn, "SELECT * FROM activity_logs WHERE board_id = ?", (BOARD_ID,), "activity_logs.json")
        
        # 3. agent_boards.json
        export_table(conn, "SELECT * FROM agent_boards WHERE board_id = ?", (BOARD_ID,), "agent_boards.json")
        
        # 4. agents.json
        export_table(conn, "SELECT * FROM agents WHERE id IN (SELECT agent_id FROM agent_boards WHERE board_id = ?)", (BOARD_ID,), "agents.json")
        
        # 5. cards.json
        export_table(conn, "SELECT * FROM cards WHERE board_id = ?", (BOARD_ID,), "cards.json")
        
        # 6. ideations.json
        export_table(conn, "SELECT * FROM ideations WHERE board_id = ?", (BOARD_ID,), "ideations.json")
        
        # 7. ideation_history.json
        export_table(conn, "SELECT h.* FROM ideation_history h JOIN ideations parent ON h.ideation_id = parent.id WHERE parent.board_id = ?", (BOARD_ID,), "ideation_history.json")
        
        # 8. refinements.json
        export_table(conn, "SELECT * FROM refinements WHERE board_id = ?", (BOARD_ID,), "refinements.json")
        
        # 9. refinement_history.json
        export_table(conn, "SELECT h.* FROM refinement_history h JOIN refinements parent ON h.refinement_id = parent.id WHERE parent.board_id = ?", (BOARD_ID,), "refinement_history.json")
        
        # 10. specs.json
        export_table(conn, "SELECT * FROM specs WHERE board_id = ?", (BOARD_ID,), "specs.json")
        
        # 11. spec_history.json
        export_table(conn, "SELECT h.* FROM spec_history h JOIN specs parent ON h.spec_id = parent.id WHERE parent.board_id = ?", (BOARD_ID,), "spec_history.json")
        
        # 12. sprints.json
        export_table(conn, "SELECT * FROM sprints WHERE board_id = ?", (BOARD_ID,), "sprints.json")
        
        # 13. sprint_history.json
        export_table(conn, "SELECT h.* FROM sprint_history h JOIN sprints parent ON h.sprint_id = parent.id WHERE parent.board_id = ?", (BOARD_ID,), "sprint_history.json")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
