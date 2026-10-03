from crewai import Agent


def build_agents(llm):
    """Create focused agents for a defensive, evidence-led triage workflow."""
    log_agent = Agent(
        role="Security Log Analyst",
        goal="Extract observed facts, suspicious indicators, and data gaps from the supplied log summary.",
        backstory="You are a careful SOC analyst. You distinguish evidence from assumptions and never invent events.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    correlation_agent = Agent(
        role="Incident Correlation Analyst",
        goal="Connect related events into a plausible timeline and explain what remains uncertain.",
        backstory="You specialize in correlating authentication, network, and system events without overstating conclusions.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    risk_agent = Agent(
        role="Cyber Risk Assessor",
        goal="Assess severity and confidence using only the provided evidence.",
        backstory="You provide cautious, explainable triage and identify missing information.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    response_agent = Agent(
        role="Incident Response Advisor",
        goal="Prepare prioritized defensive recommendations for a human analyst to review.",
        backstory="You recommend reversible, proportionate steps and require human approval for all real-world actions.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    return log_agent, correlation_agent, risk_agent, response_agent
