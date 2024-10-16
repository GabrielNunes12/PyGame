class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.offset = [0, 0]

    def update(self, target_rect):
        self.offset[0] = target_rect.centerx - self.width // 2
        self.offset[1] = target_rect.centery - self.height // 2

        # Clamp the camera to the world boundaries
        self.offset[0] = max(0, min(self.offset[0], self.world_width - self.width))
        self.offset[1] = max(0, min(self.offset[1], self.world_height - self.height))