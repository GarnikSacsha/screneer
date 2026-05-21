from app.domain.entities import AnomalyEvent


def format_telegram_event(event: AnomalyEvent) -> str:
    title = f"<b>{event.severity.upper()}: {event.event_type}</b>"
    target = event.symbol or event.sector or event.scope
    lines = [
        title,
        f"Target: {target}",
        f"Score: {event.score:.2f}",
        event.message,
    ]
    return "\n".join(lines)
