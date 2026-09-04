
# themes.py
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------------
# 主题配置文件
# 使用前需在 config.py 中设置 SELECTED_THEME
# 所有主题的完整配置字典
#---------------------------------------------------------------------------------------------

THEME_CONFIGS = {
    "GENERAL_THEME": {
        "theme_mapping"  : {
           
        },

        "theme_starters" : {
           
        }
    },
    
    "CHILDHOOD_FUN_THEME1K":{
        "theme_mapping" :{
            'school project': ['school', 'paper', 'draw', 'color', 'friend', 'work'],   # 学校活动类 
            'class pet': ['class', 'animal', 'care', 'water', 'feed', 'play'],
            'lunch break': ['food', 'friend', 'table', 'share', 'laugh', 'talk'],
            'art class': ['draw', 'paper', 'color', 'paint', 'hand', 'picture'],
            'sports day': ['run', 'play', 'ball', 'team', 'friend', 'win'],
            
            'park play': ['park', 'friend', 'run', 'play', 'tree', 'laugh'],            # 朋友互动类
            'secret game': ['friend', 'hide', 'find', 'secret', 'laugh', 'place'],
            'tree house': ['tree', 'house', 'build', 'friend', 'wood', 'play'],
            'bike ride': ['bike', 'friend', 'ride', 'road', 'wind', 'laugh'],
            'rainy game': ['rain', 'inside', 'game', 'play', 'friend', 'laugh'],
            
            'garden find': ['garden', 'flower', 'find', 'bug', 'small', 'watch'],       # 自然探索类
            'beach day': ['water', 'sun', 'sand', 'play', 'wave', 'fun'],
            'forest walk': ['forest', 'walk', 'tree', 'animal', 'path', 'see'],
            'firefly night': ['night', 'light', 'catch', 'jar', 'dark', 'watch'],
            'snow play': ['snow', 'cold', 'play', 'friend', 'build', 'laugh'],
            
            'helping mom': ['mom', 'help', 'work', 'home', 'clean', 'smile'],           # 日常小事类
            'pet care': ['dog', 'pet', 'water', 'food', 'care', 'love'],
            'baking day': ['food', 'make', 'oven', 'smell', 'eat', 'family'],
            'library visit': ['book', 'read', 'story', 'page', 'quiet', 'learn'],
            'bedtime fear': ['bed', 'dark', 'night', 'sound', 'fear', 'call']
        },
        "theme_starters" : {
            # 学校活动类 
            'school project': ["My friend hands me blue paper..."],
            'class pet': ["The small animal looks up with black eyes..."],
            'lunch break': ["My friend shares an apple with me..."],
            'art class': ["Red paint gets on my left hand..."],
            'sports day': ["The ball flies over my head..."],

            # 朋友互动类
            'park play': ["We run under the big green tree..."],
            'secret game': ["My friend whispers behind the wall..."],
            'tree house': ["Wood pieces lie on the ground..."],
            'bike ride': ["Wind plays with my hair as we..."],
            'rainy game': ["Rain taps the window while we..."],

            # 自然探索类
            'garden find': ["A red bug crawls on my finger..."],
            'beach day': ["Wet sand feels cold under my feet..."],
            'forest walk': ["Animal eyes watch from the dark..."],
            'firefly night': ["Yellow lights dance in the dark..."],
            'snow play': ["Cold snow falls on my red face..."],

            # 日常小事类
            'helping mom': ["Mom hands me a wet cloth to..."],
            'pet care': ["My dog puts his head on my..."],
            'baking day': ["Sweet smell fills the small kitchen..."],
            'library visit': ["The book opens with a soft sound..."],
            'bedtime fear': ["A strange sound comes from the dark..."]
        }
    },

    "CHILDHOOD_FUN_THEME2K": {
        "theme_mapping" : {
            'magic garden': ['flower', 'secret', 'path', 'discover', 'green', 'hide'],
            'beach treasure': ['sand', 'hole', 'shiny', 'dig', 'wave', 'surprise'],
            'puppy rescue': ['whine', 'puppy', 'bush', 'cold', 'carry', 'home'],
            'rainy adventure': ['cloud', 'puddle', 'boots', 'jump', 'laugh', 'wet'],
            "grandpa's story": ['chair', 'old', 'war', 'listen', 'eye', 'remember'],
            'treehouse secret': ['wood', 'climb', 'high', 'find', 'book', 'map'],
            'lost kitten': ['meow', 'box', 'rain', 'follow', 'kind', 'save'],
            'cookie mystery': ['kitchen', 'jar', 'empty', 'clue', 'crumb', 'solve'],
            'camping surprise': ['tent', 'dark', 'noise', 'flashlight', 'animal', 'safe'],
            'birthday magic': ['present', 'shake', 'ribbon', 'open', 'wish', 'true'],
            'library ghost': ['quiet', 'page', 'rustle', 'shadow', 'brave', 'discover'],
            'snow friend': ['cold', 'snow', 'build', 'carrot', 'stick', 'smile'],
            'frog prince': ['pond', 'catch', 'green', 'kiss', 'change', 'prince'],
            'broken wing': ['bird', 'fall', 'hurt', 'help', 'nest', 'fly'],
            'midnight snack': ['moon', 'hungry', 'tiptoe', 'fridge', 'cheese', 'giggle'],
            'message bottle': ['beach', 'glass', 'paper', 'write', 'sea', 'hope'],
            'hidden cave': ['rock', 'open', 'dark', 'treasure', 'gold', 'dragon'],
            'parade float': ['color', 'music', 'crowd', 'wave', 'smile', 'sun'],
            'magic paint': ['brush', 'wall', 'draw', 'come alive', 'chase', 'fun'],
            'island quest': ['boat', 'row', 'shore', 'map', 'palm', 'discover'],
            'circus mouse': ['tent', 'tiny', 'acrobat', 'cheer', 'clap', 'star'],
            'sunflower giant': ['seed', 'grow', 'tall', 'cloud', 'climb', 'view'],
            'moon rabbit': ['night', 'white', 'hop', 'moon', 'dream', 'follow'],
            'robot friend': ['box', 'wires', 'button', 'beep', 'help', 'fix'],
            'pirate map': ['paper', 'old', 'X', 'dig', 'sand', 'coin']
        },

        "theme_starters" : {
            'magic garden': ["Behind the old oak tree, I found a tiny door covered in vines... "],
            'beach treasure': ["My toes sank in wet sand when something shiny caught my eye... "],
            'puppy rescue': ["A soft whimper came from under the thorny bushes near the park... "],
            'rainy adventure': ["Splash! My yellow boots landed right in the biggest puddle... "],
            "grandpa's story": ["Grandpa's rocking chair creaked as he began, 'During the war...' "],
            'treehouse secret': ["Up in our secret treehouse, I noticed a loose floorboard... "],
            'lost kitten': ["Meow! The sound came from a soggy cardboard box in the alley... "],
            'cookie mystery': ["The cookie jar was full last night, but now it sat empty... "],
            'camping surprise': ["Something rustled outside our tent just as the flashlight died... "],
            'birthday magic': ["The wrapped box shook all by itself on my birthday morning... "],
            'library ghost': ["Shhh! I heard pages turning in the empty library corner... "],
            'snow friend': ["Our snowman winked at me when I placed the carrot nose... "],
            'frog prince': ["The slimy green frog looked at me and said 'Kiss me!'... "],
            'broken wing': ["A thump on the window revealed a bird with drooping wings... "],
            'midnight snack': ["Moonlight painted stripes on the kitchen floor at midnight... "],
            'message bottle': ["A glass bottle with rolled paper inside washed ashore... "],
            'hidden cave': ["The boulder rolled aside with a rumble, revealing darkness... "],
            'parade float': ["Our flower-covered float started to wobble down Main Street... "],
            'magic paint': ["The dinosaur I painted on my wall blinked its big eyes... "],
            'island quest': ["Our tiny boat bumped against a beach with golden sand... "],
            'circus mouse': ["A tiny mouse in sparkly pants balanced on a tightrope... "],
            'sunflower giant': ["My sunflower grew taller than our house overnight... "],
            'moon rabbit': ["A white rabbit hopped across the moon's face last night... "],
            'robot friend': ["The box from Uncle Joe beeped and rattled all by itself... "],
            'pirate map': ["Grandpa's old trunk held a map with a big red X... "]
        }
    },
    "CHILDHOOD_FUN_THEME3K": {
        "theme_mapping" : {
            'bicycle trail adventure':['bike', 'trail', 'wheel', 'ride', 'hill', 'mud'],
            'garden harvest day': ['garden', 'seed', 'tomato', 'pick', 'vine', 'basket'],
            'sunday pancake breakfast': ['pan', 'batter', 'flip', 'syrup', 'stack', 'table'],
            'library book mystery': ['library', 'book', 'page', 'shelf', 'find', 'worry'],
            'family pizza night': ['dough', 'oven', 'cheese', 'slice', 'topping', 'table'],
            'rainy day fort': ['rain', 'blanket', 'pillow', 'build', 'inside', 'storm'],
            'school art project': ['paint', 'paper', 'brush', 'color', 'draw', 'messy'],
            'lemonade stand adventure': ['lemon', 'cup', 'stand', 'coin', 'sell', 'hot'],
            'backyard campout': ['tent', 'fire', 'star', 'sleep', 'marshmallow', 'story'],
            'bike repair challenge': ['bike', 'chain', 'wheel', 'fix', 'grease', 'ride'],
            'neighborhood clean-up': ['street', 'pick', 'glove', 'bag', 'community', 'trash'],
            'fishing trip surprise': ['pond', 'line', 'tug', 'fish', 'net', 'rod'],
            'cookie baking time': ['cookie', 'oven', 'mix', 'batter', 'sweet', 'bake'],
            'school science fair': ['experiment', 'tube', 'watch', 'result', 'bubble', 'fair'],
            'hidden treehouse secret': ['tree', 'paper', 'hide', 'find', 'clue', 'write'],
            'grandpas workshop': ['tool', 'wood', 'build', 'nail', 'measure', 'cut'],
            'beach sandcastle day': ['sand', 'castle', 'wave', 'dig', 'tower', 'water'],
            'puppy rescue mission': ['puppy', 'lawn', 'track', 'find', 'call', 'happy'],
            'school play rehearsal': ['costume', 'script', 'stage', 'practice', 'line', 'nervous'],
            'family hiking trip': ['trail', 'walk', 'hill', 'snack', 'rest', 'path'],
            'stormy night experience': ['storm', 'dark', 'light', 'family', 'game', 'candle'],
            'bike parade fun': ['bike', 'flag', 'ride', 'crowd', 'cheer', 'street'],
            'secret recipe discovery': ['recipe', 'ingredient', 'mix', 'oven', 'taste', 'family'],
            'vegetable garden help': ['plant', 'shovel', 'dirt', 'water', 'grow', 'garden'],
            'lost toy search': ['toy', 'search', 'find', 'lawn', 'under', 'bed']
        },

        "theme_starters" : {
            'bicycle trail adventure': ["My bike wheel slid in the mud just as we reached the steep hill... "],
            'garden harvest day': ["Red juice squirted when I pulled the biggest tomato from the vine... "],
            'sunday pancake breakfast': ["The pancake batter bubbled in the pan when I turned the heat too high... "],
            'library book mystery': ["My library book wasn't on the shelf where I was sure I left it... "],
            'family pizza night': ["Cheese oozed over the edge when the pizza dough stretched too thin... "],
            'rainy day fort': ["Thunder rattled the windows as we built our pillow fort in the living room... "],
            'school art project': ["Blue paint dripped onto my shirt as I reached for the red brush... "],
            'lemonade stand adventure': ["Ice cubes clinked in the pitcher when our first customer walked up... "],
            'backyard campout': ["My marshmallow caught fire when I held it too close to the flames... "],
            'bike repair challenge': ["Grease covered my hands when the bike chain suddenly snapped... "],
            'neighborhood clean-up': ["My trash bag tore open just as we reached the corner street... "],
            'fishing trip surprise': ["The fishing line pulled tight when something big tugged underwater... "],
            'cookie baking time': ["Flour puffed into the air when I poured it into the mixing bowl... "],
            'school science fair': ["The clear liquid bubbled higher than our teacher said it should... "],
            'hidden treehouse secret': ["Under a loose floorboard, I found a folded paper with messy writing... "],
            'grandpas workshop': ["Sawdust covered my clothes as Grandpa showed me how to cut wood... "],
            'beach sandcastle day': ["My sand tower wobbled when the first wave reached our moat... "],
            'puppy rescue mission': ["A small whimper came from under the neighbor's front porch steps... "],
            'school play rehearsal': ["My costume ripped just as I was about to say my big line... "],
            'family hiking trip': ["My shoe slipped on a wet rock halfway up the hill trail... "],
            'stormy night experience': ["All the lights went out when the loudest thunder cracked overhead... "],
            'bike parade fun': ["Streamers flew off my bike when I pedaled faster down Main Street... "],
            'secret recipe discovery': ["Grandma's recipe card had a mysterious stain on the instructions... "],
            'vegetable garden help': ["Water splashed everywhere as we planted seeds in the garden rows... "],
            'lost toy search': ["Something blue peeked from under the bed where I'd already looked twice... "]
        }
    },

    "CHILDHOOD_FUN_THEME4K": {
        "theme_mapping" : {
            'baking disaster': ['oven', 'mix', 'flour', 'cookie', 'mess', 'sweet'],
            'garden harvest': ['tomato', 'seed', 'plant', 'pick', 'dirt', 'vine'],
            'bike repair challenge': ['bike', 'chain', 'wheel', 'fix', 'grease', 'ride'],
            'rainy day fort': ['rain', 'blanket', 'pillow', 'build', 'indoors', 'storm'],
            'lost library book': ['book', 'library', 'page', 'find', 'shelf', 'worry'],
            'family pizza night': ['dough', 'cheese', 'oven', 'table', 'topping', 'slice'],
            'school art project': ['paint', 'paper', 'brush', 'messy', 'color', 'draw'],
            'camping tent trouble': ['tent', 'pole', 'rain', 'stake', 'wind', 'sleep'],
            'lemonade stand success': ['lemon', 'cup', 'table', 'coin', 'sell', 'hot'],
            'broken window mystery': ['window', 'crack', 'ball', 'find', 'glass', 'who'],
            'hidden treehouse note': ['tree', 'paper', 'write', 'hide', 'find', 'clue'],
            'grandpas workshop': ['tool', 'wood', 'saw', 'build', 'nail', 'measure'],
            'beach sandcastle contest': ['sand', 'castle', 'wave', 'tower', 'dig', 'prize'],
            'sunday morning pancakes': ['pan', 'batter', 'flip', 'syrup', 'table', 'stack'],
            'soccer game mishap': ['ball', 'field', 'kick', 'mud', 'score', 'team'],
            'school science experiment': ['mix', 'bubble', 'tube', 'watch', 'react', 'result'],
            'lost puppy search': ['puppy', 'lawn', 'call', 'track', 'find', 'happy'],
            'fishing trip surprise': ['rod', 'pond', 'line', 'tug', 'fish', 'net'],
            'cookie jar mystery': ['jar', 'empty', 'crumb', 'clue', 'find', 'taste'],
            'bicycle parade fun': ['bike', 'flag', 'streamer', 'ride', 'crowd', 'cheer'],
            'secret family recipe': ['paper', 'ingredient', 'mix', 'oven', 'smell', 'taste'],
            'stormy power outage': ['dark', 'candle', 'flashlight', 'storm', 'family', 'game'],
            'backyard campout': ['tent', 'fire', 'marshmallow', 'story', 'sleep', 'star'],
            'community garden help': ['flower', 'shovel', 'plant', 'water', 'grow', 'neighbor'],
            'school play rehearsal': ['costume', 'script', 'stage', 'practice', 'line', 'nervous']
        },

        "theme_starters" : {
            'baking disaster': ["Flour flew everywhere when I opened the oven door too fast... "],
            'garden harvest': ["My hands got muddy pulling the biggest red tomato off the vine... "],
            'bike repair challenge': ["The bike chain slipped off just as I was going down the hill... "],
            'rainy day fort': ["Thunder boomed outside our blanket fort in the living room... "],
            'lost library book': ["The library book was due today, but it wasn't on my shelf... "],
            'family pizza night': ["Cheese oozed over the edge of the pizza crust in the oven... "],
            'school art project': ["Blue paint dripped onto my shoes while I reached for yellow... "],
            'camping tent trouble': ["Wind shook our tent poles during the nighttime rainstorm... "],
            'lemonade stand success': ["Ice cubes clinked in our pitcher as the first customer walked up... "],
            'broken window mystery': ["A loud crack came from the living room after I kicked the ball... "],
            'hidden treehouse note': ["Under the floorboard, I found a folded paper with messy writing... "],
            'grandpas workshop': ["Sawdust filled the air as Grandpa showed me how to cut wood... "],
            'beach sandcastle contest': ["My sand tower collapsed just as the judge walked by... "],
            'sunday morning pancakes': ["The first pancake stuck to the pan when I flipped it too soon... "],
            'soccer game mishap': ["My shoe slipped in the muddy field during the big kick... "],
            'school science experiment': ["The clear liquids bubbled higher than the teacher said they would... "],
            'lost puppy search': ["A small whimper came from under the neighbor's porch steps... "],
            'fishing trip surprise': ["My fishing rod bent almost double when something big tugged... "],
            'cookie jar mystery': ["The cookie jar lid was off, and only crumbs were left inside... "],
            'bicycle parade fun': ["Streamers flew off my bike handlebars when I pedaled faster... "],
            'secret family recipe': ["Grandma's old recipe card had a mysterious stain on the instructions... "],
            'stormy power outage': ["All the lights went out just as the thunder cracked loudest... "],
            'backyard campout': ["My marshmallow caught fire when I held it too close... "],
            'community garden help': ["Water splashed everywhere as we tried to plant new flowers... "],
            'school play rehearsal': ["My costume ripped just before my big line on stage... "]
        }
    },

    "CHILDHOOD_FUN_THEME5K": {
        "theme_mapping" : {
            'community garden project': ['garden', 'plant', 'seed', 'shovel', 'dirt', 'neighbor'],
            'bicycle repair adventure': ['bike', 'chain', 'wheel', 'fix', 'grease', 'ride'],
            'sunday pancake breakfast': ['pan', 'batter', 'flip', 'syrup', 'stack', 'table'],
            'lost library book hunt': ['library', 'book', 'shelf', 'find', 'page', 'worry'],
            'family pizza night': ['dough', 'oven', 'cheese', 'topping', 'slice', 'table'],
            'rainy day fort building': ['rain', 'blanket', 'pillow', 'build', 'indoors', 'storm'],
            'school art class': ['paint', 'paper', 'brush', 'color', 'draw', 'messy'],
            'lemonade stand success': ['lemon', 'cup', 'table', 'coin', 'sell', 'hot'],
            'backyard camping': ['tent', 'fire', 'star', 'sleep', 'marshmallow', 'story'],
            'broken window mystery': ['window', 'crack', 'ball', 'find', 'glass', 'who'],
            'neighborhood clean-up': ['trash', 'street', 'pick', 'glove', 'bag', 'community'],
            'fishing trip surprise': ['rod', 'pond', 'line', 'tug', 'fish', 'net'],
            'cookie baking time': ['cookie', 'oven', 'batter', 'mix', 'bake', 'sweet'],
            'bicycle parade fun': ['bike', 'flag', 'streamer', 'ride', 'crowd', 'cheer'],
            'secret recipe discovery': ['paper', 'ingredient', 'mix', 'oven', 'taste', 'family'],
            'stormy power outage': ['dark', 'candle', 'flashlight', 'storm', 'game', 'family'],
            'hidden treehouse note': ['tree', 'paper', 'hide', 'find', 'clue', 'write'],
            'grandpas workshop day': ['tool', 'wood', 'saw', 'build', 'nail', 'measure'],
            'sandcastle competition': ['sand', 'castle', 'wave', 'dig', 'tower', 'prize'],
            'school science fair': ['experiment', 'tube', 'mix', 'watch', 'result', 'bubble'],
            'puppy rescue mission': ['puppy', 'lawn', 'call', 'track', 'find', 'happy'],
            'school play practice': ['costume', 'script', 'stage', 'nervous', 'line', 'practice'],
            'family hiking trip': ['trail', 'walk', 'hill', 'water', 'snack', 'rest'],
            'vegetable harvest': ['tomato', 'garden', 'pick', 'vine', 'basket', 'fresh'],
            'neighborhood tag': ['run', 'chase', 'hide', 'yard', 'laugh', 'base']
        },

        "theme_starters" : {
            'community garden project': ["My shovel hit something hard in the dirt as we planted new seeds... "],
            'bicycle repair adventure': ["Grease covered my hands when the bike chain suddenly snapped... "],
            'sunday pancake breakfast': ["The first pancake stuck to the pan when I flipped it too soon... "],
            'lost library book hunt': ["My library book wasn't on the shelf where I left it yesterday... "],
            'family pizza night': ["Cheese oozed over the edge when the pizza dough stretched too thin... "],
            'rainy day fort building': ["Thunder boomed outside our blanket fort in the living room... "],
            'school art class': ["Green paint dripped onto my shoes as I reached for the red... "],
            'lemonade stand success': ["Ice cubes clinked in our pitcher as the first customer walked up... "],
            'backyard camping': ["My marshmallow caught fire when I held it too close to the flame... "],
            'broken window mystery': ["A loud crack came from the living room after the ball flew... "],
            'neighborhood clean-up': ["My trash bag tore open just as we reached the corner street... "],
            'fishing trip surprise': ["My fishing rod bent nearly double when something big tugged... "],
            'cookie baking time': ["Flour flew everywhere when I opened the oven door too fast... "],
            'bicycle parade fun': ["Streamers flew off my bike handlebars when I pedaled faster... "],
            'secret recipe discovery': ["Grandma's old recipe card had a mysterious stain on the instructions... "],
            'stormy power outage': ["All the lights went out just as the thunder cracked loudest... "],
            'hidden treehouse note': ["Under the floorboard, I found a folded paper with messy writing... "],
            'grandpas workshop day': ["Sawdust filled the air as Grandpa showed me how to cut wood... "],
            'sandcastle competition': ["My sand tower collapsed just before the judge walked by... "],
            'school science fair': ["The clear liquids bubbled higher than the teacher said they would... "],
            'puppy rescue mission': ["A small whimper came from under the neighbor's porch steps... "],
            'school play practice': ["My costume ripped just before my big line on stage... "],
            'family hiking trip': ["My shoe slipped on a wet rock halfway up the hill trail... "],
            'vegetable harvest': ["Red juice squirted when I pulled the biggest tomato off the vine... "],
            'neighborhood tag': ["My foot slipped in the wet grass just as I was almost safe... "]
        }
    },

    "OTHER_THEME": {
        "theme_mapping" : {   
           
        },

        "theme_starters" : {
            
        }
    }
}

