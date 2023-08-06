def context(hub, ctx):
    ctx.version_number = "1.0.0"

    ctx.welcome = f"Welcome to {ctx.project_name}'s Documentation!"
    ctx.welcome = f"{ctx.welcome}\n{'=' * len(ctx.welcome)}\n"

    return ctx
