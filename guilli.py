#!/usr/bin/env python
'''
version 0.2
+ added hall of fame
'''

import sys, pygame, random, time, GameObject, GameArea, GameSound, re

_major_version_ = 0
_minor_version_ = 2
_score_filename = 'score.txt'
screen_color = 0, 0, 0

default_text_color = 255, 255, 255
username_color = 128,128,255

username = 'Unnamed'

inc = lambda x: x+1
dec = lambda x: x-1

def quit_game():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.display.quit()
    pygame.font.quit
    pygame.quit()
    

def handle_keys():
    """ event handler """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
            

def init_screen():
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('LUKANOID v.%d.%d' % (_major_version_, _minor_version_))
    return screen


def create_level(area):
    # create balls
    balls = [GameObject.Ball(area, 100, 20), GameObject.Ball(area, 120,40)]

    # create bricks
    random.seed(abs(time.time()))
    bricksOnLevel = random.randint(15, 30)
    bricks = []
    i=0
    while (i<bricksOnLevel):
        collide = True
        while collide:
            new_b = GameObject.random_brick_at_random_place(area, i)
            collide = False
            for b in bricks:
                if new_b.rect.colliderect(b.rect):  collide = True
        bricks.append( new_b )
        i = inc(i)

    return balls, bricks

def play_level(area, lev, balls, bricks, platform, score):
    clock = pygame.time.Clock()
    while 1:
        handle_keys()
        area.screen.fill(screen_color)
        area.paint()
        platform.control()
        if not any( [platform.newrect.colliderect(brick.rect) for brick in bricks] ):
            platform.finish_move()

        platform.paint(area.screen)

        for ball in balls:
            ball.start_move()
            ball.check_collision(platform)
            ball.paint(area.screen)
            for brick in bricks:
                ball.check_collision(brick)
                if brick.deleted:
                    score +=brick.score
                    bricks.remove(brick)
                    del brick
                else:
                    brick.paint(area.screen)
            ball.finish_move()
            if ball.deleted:
                balls.remove(ball)
                del ball

        if len(bricks) == 0:
            return True, score

        if len(balls) == 0:
            return False, score

        print_info(area.screen, lev, score)
        pygame.display.flip()
        clock.tick(70)

        
def wait_for_enter():
    key = pygame.key.get_pressed()
    while not (key[pygame.K_RETURN] or key[pygame.K_KP_ENTER]):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        pygame.time.wait(1)

        
def show_title(screen, string, size):
    screen.fill(screen_color)
    font = pygame.font.Font(None, size)
    title = font.render(string,1,default_text_color)

    font = pygame.font.Font(None, 20)
    caption = font.render("press Enter to continue.", 1, default_text_color);

    scr_w,scr_h = screen.get_size()
    title_w, title_h = title.get_size()
    capt_w, capt_h = caption.get_size()

    screen.blit(title, (scr_w/2 - title_w/2,150))
    screen.blit(caption, (scr_w/2 - capt_w/2,200))
    pygame.display.flip()
    
    wait_for_enter()

    
def print_info(screen, level, score):
    font = pygame.font.Font(None, 24)

    global username
    user_print = font.render(username, 1, username_color)
    
    level_text = "level: " + str(level)
    level_print = font.render(level_text,1,default_text_color)

    score_text = "score: " + str(score)
    score_print = font.render(score_text,1,default_text_color)

    scr_w,scr_h = screen.get_size()

    text_w, text_h = level_print.get_size()

    screen.blit(user_print, (scr_w-100, 500))
    screen.blit(level_print, (scr_w-100, 500+text_h+10))
    screen.blit(score_print, (scr_w-100, 500+(text_h+10)*2))

def save_score(username, userscore):
    f = open(_score_filename, 'rU')
    s = f.read()
    f.close()
    scorelist = re.findall('(\w+) (\d+)', s)

    score_dict = {}
    score_dict[username] = userscore
    for key, val in scorelist:
        if (not score_dict.has_key(key)) or int(val)>score_dict[key]:
            score_dict[key] = int(val)

    scorelist = [k+' '+str(v) for k,v in score_dict.items()]
    s = '\n'.join(scorelist)
    
    f = open(_score_filename,'w')

    f.write(s)
    f.close()

def show_score(screen):
    global username
    f = open(_score_filename, 'r')
    s = f.read()
    f.close()
    scorelist = re.findall('(\w+) (\d+)', s)

    screen.fill(screen_color)
    font = pygame.font.Font(None, 30)
    title = font.render("HALL OF FAME", 1, default_text_color);

    names = []
    values = []

    scorelist = sorted(scorelist, reverse=True, key=lambda x: int(x[1]))[:20]
    font = pygame.font.Font(None, 25)
    for name, score in scorelist:
        color = username_color if name == username else default_text_color
        names.append(font.render(name, 1, color));
        values.append(font.render(score, 1, color));

    scr_w,scr_h = screen.get_size()
    title_w, title_h = title.get_size()

    screen.blit(title, (scr_w/2 - title_w/2,20))
    for i in range(len(scorelist)):
        screen.blit(names[i], (50, 100+(i*font.get_height()+4)))
        screen.blit(values[i], (700, 100+(i*font.get_height()+4)))
    pygame.display.flip()
    wait_for_enter()   


def main():
    args = sys.argv[1:]
    global username
    if args[0]:
      username = args[0]
      print(username)
    screen = init_screen()
    sounds = GameSound.Sounds()
    sounds.load()

    pygame.font.init()

    show_title(screen, "LUKANOID", 42)

    area = GameArea.Area(screen)
    platform = GameObject.Platform(area)

    play = True
    levels = 0
    score = 0
    while(play):
        sounds.play_level_music()
        balls, bricks = create_level(area)
        play, score = play_level(area, levels+1, balls, bricks, platform, score)
        sounds.stop_level_music()
        if play:
            levels +=1
            sounds.play("win")
            show_title(area.screen, "level "+str(levels)+" complete!", 28)
        else:
            sounds.play("fail")
            save_score(username, score)
            show_score(screen)

        for b in balls: b.increase_speed()

    event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(event)
    quit_game()
    sys.exit()
    

if __name__ == '__main__':
    main()
