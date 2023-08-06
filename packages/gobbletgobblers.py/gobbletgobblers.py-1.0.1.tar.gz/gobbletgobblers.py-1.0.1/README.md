# install

```
pip install -U gobbletgobblers.py
```

# How To Use

## Create game

```py
from gobbletgobblers import GobbletGobblers
gobb = GobbletGobblers(FirstPlayer, SecondPlayer, EmptyBoardText)
```

> FirstPlayer - 先攻のプレイヤー  
SecondPlayer - 後攻のプレイヤー  
EmptyBoardText - 何も置かれていない場所に表示するテキスト

## Variables mean

### gobb.sen, gobb.kou
先攻、後攻プレイヤーの情報が格納

#### Attributes
> player - Create Gameの手順で設定されたプレイヤー情報  
gobbs - プレイヤーの所持している(新たに盤面に設置可能な)ゴブレット  
color - プレイヤーの色(Red / Blue)  
scolor - プレイヤーの色の略版(r / b) 基本的に内部でのみ使用  
modes - プレイヤーが選択できるモード(初期: ['p'])

### gobb.empty_board_text
Create Gameの手順で設定された文字列

### gobb.turn
現在進行しているターン数

### gobb.now_player
現在のプレイヤー  
Attributesはgobb.sen, gobb.kouと同じ

### gobb.won
勝者が出たかどうか

### gobb.winner
勝者  
Attributesはgobb.sen, gobb.kou, gobb.now_playerと同じ

### gobb.board
盤面情報

```
gobb.board
├─a1
│  ├─ t
│  ├─ b
│  ├─ m
│  └─ s
├─a2
│  ├─ t
│  ├─ b
│  ├─ m
│  └─ s
├─a3
│  ├─ t
│  ├─ b
│  ├─ m
│  └─ s
.
.
.
```

> a1, a2, a3... - 盤面の座標  
+----+----+----+  
| a1 | a2 | a3 |  
+----+----+----+  
| b1 | b2 | b3 |  
+----+----+----+  
| c1 | c2 | c3 |  
+----+----+----+  
t - top その座標におけるもっとも大きいゴブレット  
b - big 一番大きいゴブレット  
m - medium 普通サイズのゴブレット  
s - small 一番小さいゴブレット

### gobb.choices_put

putモード時に設置可能な場所を返す

```py
choices_put = gobb.choices_put()
```

### gobb.put

指定の座標に指定のサイズのゴブレットを配置

```py
gobb.put(place, size)
```

> place - 配置する座標  
size - 配置するゴブレットのサイズ

### gobb.choices_move_from

moveモード時に動かすことのできるゴブレットの座標を返す

```py
choices_move_from = gobb.choices_move_from()
```

### gobb.choices_move_to

moveモード時に指定のゴブレットを移動させられる座標を返す

```py
choices_move_to = gobb.choices_move_to(from)
```

> from - 移動前のゴブレットの座標

### gobb.move

ゴブレットを移動させる

```py
gobb.move(from, to)
```

> from - 移動前のゴブレットの座標  
to - 移動後のゴブレットの座標
