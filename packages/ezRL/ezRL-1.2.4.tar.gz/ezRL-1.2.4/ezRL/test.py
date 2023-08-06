
import sys
# from ezRL import catcher_game as c_game	# 本番環境での使用法
from relpath import add_import_path
add_import_path("../")
# Catcherゲーム [catcher_game]
from _develop_ezRL import catcher_game as c_game
# Deep Q Network AI [DQN_Agent]
from _develop_ezRL import DQN_Agent

# debug
from _develop_ezRL import TileArt
# タイルを並べた画像の作成 [ezRL]
t_art = TileArt(
	canvas_size = (300,300),
	tile_file_dic = {
		"wall": "./test_tiles/wall.bmp",
		"box": "./test_tiles/box.bmp",
		"player": "./test_tiles/player.png"
	},
	transparent_color = (255, 0, 255)	# 透過色の指定 (b,g,r)
)
# タイルの表示サイズ
tile_size = 64
# タイルを並べた画像の作成
img = t_art.gen_img([
	{"pos": (0,0), "size": (tile_size, tile_size), "texture": "wall", "layer": 1},
	{"pos": (32,0), "size": (tile_size, tile_size), "texture": "player", "layer": 2},
	{"pos": (64,64), "size": (tile_size, tile_size), "texture": "box", "layer": 1},
])
# 表示
from _develop_ezRL import show_img
show_img(img)
sys.exit()

train_ai = DQN_Agent(action_ls = c_game.action_ls, ai_obs = c_game.ai_obs) # Deep Q Network AI
episode_n = 700	# エピソード数
total_reward_ls = []
for episode_idx in range(episode_n):
	# state, actionの初期化
	action, state = "initial_action", c_game.gen_init_state(game_params = {})
	reward_ls = []
	# ゲーム進行
	while state["finished"] is False:
		state, reward = c_game.game_step(state, action)
		action = train_ai.think(state, reward) # 行動決定
		reward_ls.append(reward)
	total_reward_ls.append(sum(reward_ls))
	print("Episode #%d, Reward: %.1f"%(episode_idx, total_reward_ls[-1]))
# 獲得報酬の推移を表示
from matplotlib import pyplot as plt
plt.plot(total_reward_ls)
plt.show()
# state, actionの初期化
action, state = "initial_action", c_game.gen_init_state(game_params = {})
# テストプレイ
while state["finished"] is False:
	human_obs(state, waitKey_msec = 100) # 人間用の観測関数
	state, reward = c_game.game_step(state, action)
	action = train_ai.think(state, reward)


sys.exit()

#### 以下、ちゃんとtestとtrainが分かれている例


from __init__ import RandomPlayer	# 開発時




# ランダムAI
train_ai = RandomPlayer(action_ls = ["act_0", "act_1"])

# 学習
for _ in range(3):
	action = train_ai.think(state = None, reward = 1)
	print(action)

# テスト用プレーヤーを生成
test_ai = train_ai.gen_test()

# テスト
for _ in range(3):
	action = test_ai.think(state = None, reward = 1)
	print(action)

sys.exit()

######### 以下、未整備

# # debug用人間プレーヤー
# from ezRL import HumanPlayer
# # 学習用AI, 対戦フィールド (arena)
# from ezRL import DQN_AI, arena
# # テスト用ゲーム (紅白ゲーム)
# from ezRL import RW_Game

# # # debug用人間プレーヤー
# # human_p = HumanPlayer(action_dic = {"Red": [1,0], "White": [0,1]})
# # game = RW_Game(round_n = 5)	# テスト用ゲーム (紅白ゲーム)
# # # 対戦して学習
# # arena(game, [human_p])	# 対戦フィールド (arena)
# # sys.exit()

# train_ai = DQN_AI(action_dim = 2)	# 学習用AI
# game = RW_Game(round_n = 100)	# テスト用ゲーム (紅白ゲーム)
# # 対戦して学習
# arena(game, [train_ai])	# 対戦フィールド (arena)

# # テスト用プレーヤーを生成
# test_ai = train_ai.gen_test()
# game = RW_Game(round_n = 100)	# テスト用ゲーム (紅白ゲーム)
# # 対戦して性能テスト (学習済みAI)
# arena(game, [test_ai])	# 対戦フィールド (arena)
