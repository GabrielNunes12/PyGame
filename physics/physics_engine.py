class PhysicsEngine:
    def __init__(self, gravity=0.8, terminal_velocity=20):
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity

    def apply_gravity(self, obj, gravity=None):
        if gravity is None:
            gravity = self.gravity
        obj['velocity_y'] += gravity
        if obj['velocity_y'] > self.terminal_velocity:
            obj['velocity_y'] = self.terminal_velocity
        obj['y'] += obj['velocity_y']