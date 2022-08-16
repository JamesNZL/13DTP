''' Platformer Game '''

# Import arcade python library
import arcade

# Constant variables relevant to window display
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'Platformer'

# Constant variables relevant to game physics and display
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
GEM_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 13

# Constant variables defining side-scrolling margins
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 75
TOP_VIEWPORT_MARGIN = 100

# Constant variables that define player's spawn coordinates
PLAYER_START_X = 320
PLAYER_START_Y = 192

# Constant variables to assign boolean system to charcter's direction
RIGHT_FACING = 0
LEFT_FACING = 1

# File address of player sprite on respective levels
CHARACTER_LIST = {
    1: 'female_adventurer/femaleAdventurer',
    2: 'zombie/zombie',
    3: 'robot/robot'
}

# Constant variables for the game's grid system
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Total number of levels in the game
TOTAL_LEVELS = 3

# Total number of lives before game over
MAX_LIVES = 10

# Offset of 'map exit' sprite from the edge of the world
MAP_END_OFFSET = 4.5

# 'a' value of Desmos equation (see documentation)
SCORE_SCALE = -350

# 'b' value of Desmos equation (see documentation)
SCORE_SHIFT = 15

def load_texture_pair(filename):
    ''' Load a pair of textures, mirroring the original '''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(arcade.Sprite):
    ''' Player Sprite '''

    def __init__(self, level):
        ''' Run when a player character is created '''
        # Inherit all variables from __init__() of arcade.Sprite
        super().__init__()

        # Spawn character facing to the right
        self.character_face_direction = RIGHT_FACING

        # Iterative variable to cycle between animated image sequences
        self.cur_texture = 0

        # Scale character as per game constant
        self.scale = CHARACTER_SCALING

        # Variables to store character's movement state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # Main path of arcade's character resources
        main_path = ':resources:images/animated_characters/{}'.format(CHARACTER_LIST[level])

        # Load the character's textures for jumping, falling and standing
        self.idle_texture_pair = load_texture_pair('{}_idle.png'.format(main_path))
        self.jump_texture_pair = load_texture_pair('{}_jump.png'.format(main_path))
        self.fall_texture_pair = load_texture_pair('{}_fall.png'.format(main_path))

        # Load the character's walking textures and store in a list
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair('{}_walk{}.png'.format(main_path,i))
            self.walk_textures.append(texture)

        # Load the character's climbing textures and store in a list
        self.climbing_textures = []
        texture = arcade.load_texture('{}_climb0.png'.format(main_path))
        self.climbing_textures.append(texture)
        texture = arcade.load_texture('{}_climb1.png'.format(main_path))
        self.climbing_textures.append(texture)

        # Set the spawn texture
        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time): #delta_time: Time interval since previous function call in seconds.
        ''' Method to set the animation's graphical state depending on its action '''
        # Change the direction the character is facing if necessary
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Animation for climbing
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1: #abs returns the absolute value, i.e. -20 would return 20
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Animation for jumping, and is dependant on whether the sprite is on a ladder or not
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Animation for idling
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Animation for walking
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class GameOverView(arcade.View):
    ''' Displays a game over screen '''

    def __init__(self, display, gems, minutes, seconds, millis, lives):
        ''' Run when an end screen is created '''
        # Inherit all variables from __init__() of arcade.View
        super().__init__()

        # Load specified game over screen
        self.texture = arcade.load_texture('{}.png'.format(display))
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0 , SCREEN_HEIGHT - 1)

        # Variables to store game results
        self.gems = gems
        self.minutes = minutes
        self.seconds = seconds
        self.millis = millis
        self.lives = lives

        # Ensure score does not get multiplied by 0
        if self.lives == 0:
            self.lives = 0.5

        # Calculate game score using game results
        self.total_seconds = float(self.minutes*60 + self.seconds + float(self.millis))
        self.score = (((SCORE_SCALE * self.total_seconds)/(self.gems + SCORE_SHIFT))
                        + 4*SCORE_SCALE) * self.lives

        # If score function returns a negative result, use a different formula
        if self.score <= 0:
            self.score = int((self.gems * (1/self.total_seconds) * 1000) * self.lives)

    def on_draw(self):
        ''' Draws the game over screen '''
        # Draw game over screen
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

        # Draw game results text in the middle of the screen
        end_text = ('Gems: {} | Time: {:02d}:{:02d}:{} | Score: {}'.format(self.gems,
                                                                           self.minutes,
                                                                           self.seconds,
                                                                           str(self.millis)[-2:],
                                                                           self.score))
        arcade.draw_text(end_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.csscolor.BLACK, 24, align='center',
                         anchor_x='center', anchor_y='center')
     
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        ''' Restarts the game on mouse click '''
        game_view = MyGame()
        game_view.setup(game_view.level)
        self.window.show_view(game_view)


class MyGame(arcade.View):
    ''' Main application class. '''

    def __init__(self):
        ''' Run when an instance of the game is created '''
        # Inherit all variables from __init__() of arcade.View
        super().__init__()

        # Variables to store key press states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Lists to store all sprites by type
        self.gem_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.ladder_list = None

        # Variable to store player sprite
        self.player_sprite = None

        # Variable to store game physics engine
        self.physics_engine = None

        # Variables to store scrolling data
        self.view_bottom = 0
        self.view_left = 0

        # Variables to track game results
        self.gems = 0
        self.minutes = 0
        self.seconds = 0
        self.millis = 0
        self.total_time = 0.00

        # Variable to store the maximum lives allowed
        self.lives = MAX_LIVES

        # Variable to store the current level
        self.level = 1

        # Variable to store the x-coord for the end of the map
        self.end_of_map = 0

    def setup(self, level):
        ''' Sets up game to load new levels '''
        # Initialise sprite lists as objects of arcade.SpriteList
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()
        self.dont_touch_list = arcade.SpriteList()
        self.ladder_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # Set up the player sprite and store in a list
        self.player_sprite = PlayerCharacter(level)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Name of the layer containing the platforms
        platforms_layer_name = 'Platforms'
        # Name of the layer containing collectables
        gems_layer_name = 'Gems'
        # Name of the layer containing foreground textures
        foreground_layer_name = 'Foreground'
        # Name of the layer containing background textures
        background_layer_name = 'Background'
        # Name of the layer containing obstacles
        obstacles_name = 'Obstacles'
        # Name of the layer containing ladders
        ladders_layer_name = 'Ladders'

        # File directory of maps
        map_name = ('levels/map1_level_{}.tmx'.format(level))

        # Load the map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the map exit point
        self.end_of_map = (my_map.map_size.width - MAP_END_OFFSET) * GRID_PIXEL_SIZE

        # Background layer
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # Foreground layer
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)

        # Platform layer
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        # Gem layer
        self.gem_list = arcade.tilemap.process_layer(my_map,
                                                      gems_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # Obstacle layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            obstacles_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        # Ladder layer
        self.ladder_list = arcade.tilemap.process_layer(my_map,
                                                        ladders_layer_name,
                                                        TILE_SCALING,
                                                        use_spatial_hash=True)

        # Set the map's background colour
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Set the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list, 
                                                             GRAVITY, 
                                                             ladders=self.ladder_list)

    def on_draw(self):
        ''' Render the screen. '''
        # Clear the screen
        arcade.start_render()

        # Draw the map's sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.gem_list.draw()
        self.ladder_list.draw()
        self.dont_touch_list.draw()
        self.player_list.draw()
        self.foreground_list.draw()

        # Calculate the minutes elapsed
        self.minutes = int(self.total_time) // 60

        # Calculate the seconds elapsed
        self.seconds = int(self.total_time) % 60

        # Calculate the milliseconds elapsed
        self.millis = format(round(float(self.total_time) - int(self.total_time), 2), '.2f')

        # Draw game stats on the screen
        game_text = ('Gems: {} | Lives: {} | Time: {:02d}:{:02d}'.format(self.gems,
                                                                         self.lives,
                                                                         self.minutes,
                                                                         self.seconds))
        arcade.draw_text(game_text, 10 + self.view_left,
                         10 + self.view_bottom,
                        arcade.csscolor.WHITE, 24)

    def process_keychange(self):
        ''' Called when we change a key up/down or we move on/off a ladder. '''
        # Process up/down inputs
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right inputs
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        ''' Called whenever a key is pressed. '''
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        ''' Called when the user releases a key. '''
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        ''' Movement and game logic '''
        # Move the player using the physics engine
        self.physics_engine.update()

        # Update the animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.player_list.update_animation(delta_time)

        # Check for collisions with gems
        gem_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.gem_list)
        
        # Remove collected gems from the map
        for gem in gem_hit_list:
            # Remove the gem
            gem.remove_from_sprite_lists()
            # Add to the count of gems collected
            self.gems += 1

        # --- Manage Scrolling ---
        # Check if viewport needs to change
        changed = False
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.lives -= 1
            
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            self.view_left = 0
            self.view_bottom = 0
            changed = True

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to full integer values
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            # Scroll the viewport
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom)
        
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1
            # Move viewport back to the start
            self.view_left = 0
            self.view_bottom = 0
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

            if self.level <= TOTAL_LEVELS:
                # Load the next level
                self.setup(self.level)

            else:
                # Draw the game over screen
                view = GameOverView('game_over', self.gems, self.minutes,
                                    self.seconds, self.millis, self.lives)
                self.window.show_view(view)

        if self.lives == 0:
                # Draw the death screen
                view = GameOverView('death', self.gems, self.minutes,
                                    self.seconds, self.millis, self.lives)
                self.window.show_view(view)

        # Update total time
        self.total_time += delta_time


def main():
    ''' Main method '''
    # Create the game window using arcade.Window()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # Create an instance of MyGame()
    game_view = MyGame()
    # Set up game level
    game_view.setup(game_view.level)
    # Show the game level
    window.show_view(game_view)
    # Run the game
    arcade.run()


if __name__ == '__main__': # If the file is being run directly and not imported:
    # Run the program
    main()
