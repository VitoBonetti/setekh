def require_role(*allowed_roles):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            state = self.state
            if not hasattr(state, "current_role") or state.current_role not in allowed_roles:
                state.page.go("/401")
                return
            return method(self, *args, **kwargs)
        return wrapper
    return decorator
