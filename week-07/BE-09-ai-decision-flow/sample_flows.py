from workflow import WorkflowGraph, Node, Edge

SUPPORT_TRIAGE_FLOW = WorkflowGraph(
    id="support-ticket-triage",
    name="Customer Support Incident Triage",
    nodes=[
        Node(id="node-start", label="Incoming Ticket", type="start", x=50, y=150),
        Node(
            id="node-billing",
            label="Billing Check",
            type="decision",
            prompt="Is this a billing, payment, invoice, or refund inquiry?",
            x=250,
            y=150
        ),
        Node(
            id="node-urgent",
            label="Severity Check",
            type="decision",
            prompt="Is this an urgent production outage or crash?",
            x=500,
            y=250
        ),
        Node(id="outcome-billing", label="Priority Billing & Finance Queue", type="outcome", x=500, y=50),
        Node(id="outcome-oncall", label="Page Tier-3 On-Call Engineer", type="outcome", x=750, y=180),
        Node(id="outcome-standard", label="Standard Support Desk (48h SLA)", type="outcome", x=750, y=320)
    ],
    edges=[
        Edge(id="e1", source="node-start", target="node-billing", branch="DEFAULT"),
        Edge(id="e2", source="node-billing", target="outcome-billing", branch="YES"),
        Edge(id="e3", source="node-billing", target="node-urgent", branch="NO"),
        Edge(id="e4", source="node-urgent", target="outcome-oncall", branch="YES"),
        Edge(id="e5", source="node-urgent", target="outcome-standard", branch="NO")
    ]
)

SECURITY_GATE_FLOW = WorkflowGraph(
    id="pr-security-gate",
    name="Pull Request Security Gatekeeper",
    nodes=[
        Node(id="sec-start", label="New Pull Request", type="start", x=50, y=150),
        Node(
            id="sec-check",
            label="Security Audit",
            type="decision",
            prompt="Does this code introduce a security vulnerability or credential leak?",
            x=250,
            y=150
        ),
        Node(
            id="arch-check",
            label="Defect Audit",
            type="decision",
            prompt="Does this code contain a critical bug or syntax failure?",
            x=500,
            y=250
        ),
        Node(id="sec-block", label="Hard Block PR & Alert Security", type="outcome", x=500, y=50),
        Node(id="sec-warn", label="Request Senior Peer Review", type="outcome", x=750, y=180),
        Node(id="sec-approve", label="Fast-Track Auto-Approve", type="outcome", x=750, y=320)
    ],
    edges=[
        Edge(id="se1", source="sec-start", target="sec-check", branch="DEFAULT"),
        Edge(id="se2", source="sec-check", target="sec-block", branch="YES"),
        Edge(id="se3", source="sec-check", target="arch-check", branch="NO"),
        Edge(id="se4", source="arch-check", target="sec-warn", branch="YES"),
        Edge(id="se5", source="arch-check", target="sec-approve", branch="NO")
    ]
)

SAMPLE_FLOWS = {
    SUPPORT_TRIAGE_FLOW.id: SUPPORT_TRIAGE_FLOW,
    SECURITY_GATE_FLOW.id: SECURITY_GATE_FLOW
}
