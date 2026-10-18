import os
import time
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import inngest

from engine import evaluate_decision_node

inngest_client = inngest.Inngest(
    app_id="decision-flow-service",
    is_production=False
)

# In-memory execution store for polling results
RUN_HISTORY: Dict[str, Dict[str, Any]] = {}

class Node(BaseModel):
    id: str
    label: str
    type: str = "decision" # "start", "decision", "outcome"
    prompt: Optional[str] = None
    x: Optional[float] = 0
    y: Optional[float] = 0

class Edge(BaseModel):
    id: str
    source: str
    target: str
    branch: str = "YES" # "YES", "NO", "DEFAULT"

class WorkflowGraph(BaseModel):
    id: str = "flow-default"
    name: str = "AI Triage Flow"
    nodes: List[Node]
    edges: List[Edge]

class ExecutionRequest(BaseModel):
    graph: WorkflowGraph
    input_context: str

def execute_workflow_sync(graph: WorkflowGraph, input_context: str, run_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes a decision flow graph step-by-step.
    Traverses decision nodes, calls the AI evaluation engine, and branches on YES / NO edges.
    """
    if not run_id:
        run_id = f"run_{uuid.uuid4().hex[:8]}"

    node_map = {n.id: n for n in graph.nodes}
    
    # Locate starting node
    start_node = next((n for n in graph.nodes if n.type == "start"), None)
    if not start_node:
        # Find root node with in-degree 0
        targets = {e.target for e in graph.edges}
        root_candidates = [n for n in graph.nodes if n.id not in targets]
        start_node = root_candidates[0] if root_candidates else graph.nodes[0]

    trace = []
    current_node = start_node
    max_steps = 15
    steps_taken = 0
    final_outcome = None

    while current_node and steps_taken < max_steps:
        steps_taken += 1

        if current_node.type == "start":
            # Pass directly to next node
            out_edges = [e for e in graph.edges if e.source == current_node.id]
            next_id = out_edges[0].target if out_edges else None
            trace.append({
                "step": steps_taken,
                "node_id": current_node.id,
                "label": current_node.label,
                "type": "start",
                "decision": "PASSTHROUGH",
                "rationale": "Workflow execution initiated.",
                "next_node": next_id
            })
            current_node = node_map.get(next_id) if next_id else None

        elif current_node.type == "decision":
            eval_res = evaluate_decision_node(current_node.prompt or current_node.label, input_context)
            decision = eval_res["decision"] # "YES" or "NO"
            
            # Find matching edge
            matching_edge = next((e for e in graph.edges if e.source == current_node.id and e.branch.upper() == decision), None)
            
            # Fallback to default edge if strictly specific branch missing
            if not matching_edge:
                matching_edge = next((e for e in graph.edges if e.source == current_node.id and e.branch.upper() == "DEFAULT"), None)

            next_id = matching_edge.target if matching_edge else None
            
            trace.append({
                "step": steps_taken,
                "node_id": current_node.id,
                "label": current_node.label,
                "type": "decision",
                "prompt": current_node.prompt or current_node.label,
                "decision": decision,
                "rationale": eval_res["rationale"],
                "latency_ms": eval_res["latency_ms"],
                "model": eval_res["model"],
                "next_node": next_id
            })
            
            current_node = node_map.get(next_id) if next_id else None

        elif current_node.type == "outcome":
            final_outcome = current_node.label
            trace.append({
                "step": steps_taken,
                "node_id": current_node.id,
                "label": current_node.label,
                "type": "outcome",
                "decision": "TERMINAL",
                "rationale": f"Reached outcome resolution: {current_node.label}",
                "next_node": None
            })
            break

    run_record = {
        "run_id": run_id,
        "status": "COMPLETED" if final_outcome else "DEAD_END",
        "final_outcome": final_outcome or "Execution terminated without outcome node.",
        "input_context": input_context,
        "total_steps": steps_taken,
        "trace": trace,
        "executed_at": time.time()
    }
    RUN_HISTORY[run_id] = run_record
    return run_record

# Inngest Background Function Definition
@inngest_client.create_function(
    fn_id="run-ai-decision-flow",
    trigger=inngest.TriggerEvent(event="flow/execute"),
    retries=1
)
async def inngest_decision_flow(ctx: inngest.Context, step: inngest.Step) -> dict:
    event_data = ctx.event.data
    graph_dict = event_data["graph"]
    graph = WorkflowGraph(**graph_dict)
    input_context = event_data["input_context"]
    run_id = event_data.get("run_id", f"inngest_{uuid.uuid4().hex[:8]}")

    # Wrap graph traversal in Inngest step
    result = await step.run("execute-graph-traversal", lambda: execute_workflow_sync(graph, input_context, run_id))
    return result
