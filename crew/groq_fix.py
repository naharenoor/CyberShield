import litellm


def strip_marker(messages):
    cleaned = []
    for msg in messages or []:
        if isinstance(msg, dict):
            msg = {k: v for k, v in msg.items() if k != "cache_breakpoint"}
        cleaned.append(msg)
    return cleaned


original_completion = litellm.completion
original_acompletion = litellm.acompletion


def completion(*args, **kwargs):
    if "messages" in kwargs:
        kwargs["messages"] = strip_marker(kwargs["messages"])
    return original_completion(*args, **kwargs)


async def acompletion(*args, **kwargs):
    if "messages" in kwargs:
        kwargs["messages"] = strip_marker(kwargs["messages"])
    return await original_acompletion(*args, **kwargs)


litellm.completion = completion
litellm.acompletion = acompletion
