from .config import *

#---------------------------------------------------------------------------------------------
# 叙事特征数据模块
# 包含用于文本处理的各类特征数据，包括：
# - 关键词集合：用于识别文本的不同语言特征
# - 示例文本：用于语义相似度计算的标准示例
#---------------------------------------------------------------------------------------------

# 叙事类示例文本
NARRATIVE_EXAMPLES = {
    # 学校活动类
    'school project': [
        "My friend handed me blue paper. 'Draw the sky,' she said. We sat at our small table. I cut green trees with scissors. Snip-snip-snip! Paper bits flew into her hair. We laughed. Glue made my fingers sticky. We ran out! 'Can we share your glue?' Jamie asked the girls. They smiled yes. We worked until the bell rang. Jamie added yellow sun rays. I wrote 'JAMIE & SARA.' Our teacher touched my shoulder. 'Good work!' At home, Mom hung it on the fridge. 'Tell me about your day,' she said. I pointed. 'That's our sky, trees, and friend's glue!'"
    ], 
}

# 非叙事类示例文本
NON_NARRATIVE_EXAMPLES = [
    "Step-by-step explanation for:\n2x + 3y = 12\nx + y = 5... Using substitution and elimination methods.",  # 数学方程求解（教学+学术）
    "#ChildrensStory #BallGame #PlayTime #RockMusic #RockCulture #ArtisticExpression #UrbanExploration #HistoricalPreservation #StructuralDecay",  # 标签分类信息
    "**Identify the Required Elements** **Understand the Structure** **Introduce Characters** **Develop the Story** **Incorporate Events and Developments**",
    "I need to write a 279-word narrative based on the provided structure and requirements.",  # 写作思路
    "First, I'll set the scene with the family living in a small town. ...Next, I think about the characters.",
]

# 叙事类示例文本
NARRATIVE_EXAMPLES1K = {
    # 学校活动类
    'school project': [
        "While waiting in line, she accidentally drops a piece of paper on the counter, causing a firecracker to burst into view.",
        "Jamie laughed when paper bits flew into her hair.",  # From article 1
        "Jamie asked the girls next to us, 'Can we share your glue stick?'",  # From article 1
        "We put little paper people inside.",  # From article 2
        "Mrs. Clark came over. 'What a fine house!' she said.",  # From article 2
        "Ben drew the roads with a black crayon.",  # From article 3
        "We put our school right in the middle.",  # From article 3
        "She poured in vinegar. Foam bubbled up and over the top!",  # From article 4
        "It looked like real fire! Some foam dripped on the table.",  # From article 4
        "We put on our masks. 'Roar!' I said.",  # From article 5
        "After school, I showed Mom. 'What a fierce lion!' she laughed."  # From article 5
    ],
    'class pet': [
        "He knew it was food time! I put the seeds in his bowl.",  # From article 1
        "He ran over fast. His tiny paws held a seed.",  # From article 1
        "He started to run! The ball rolled across the floor.",  # From article 2
        "Kids laughed. 'Go, Fluffy!' I cleaned his cage fast.",  # From article 2
        "I got down on my knees. I saw two shiny eyes.",  # From article 3
        "I got his food bag. I shook it.",  # From article 3
        "Bump! He hit a chair leg. He turned and ran the other way.",  # From article 4
        "I gave him a drink of water. He drank a lot.",  # From article 4
        "He didn't like it! He tried to climb out.",  # From article 5
        "I used a soft cloth to wash him. He stopped struggling.",  # From article 5
    ],
    'lunch break': [
        "I opened my lunch box. Mom made my favorite! Peanut butter and jelly.",  # From article 1
        "Ben sat next to me. 'I have cookies,' he said.",  # From article 1
        "Emma opened her big lunch box. 'Here,' she said. She gave me half her cheese sandwich.",  # From article 2
        "Leo had extra grapes. He shared some with me.",  # From article 2
        "We talked about our pets. Tom has a big dog. Mia has a cat.",  # From article 3
        "We finished our pizza. The bell rang. 'Time for class,' Mia said.",  # From article 3
        "Jake had chicken nuggets. He gave me one. I gave him some noodles.",  # From article 4
        "Jake told a funny joke. I laughed so hard milk came out my nose!",  # From article 4
        "We looked at each other. I made a silly face. Sam almost laughed.",  # From article 5
        "The teacher rang a bell. 'Lunch is over!' she said."  # From article 5
    ],
    'art class': [
        "I took a blue crayon. I drew a big blue sky.",  # From article 1
        "I put a little cat in the window. 'Nice cat!' said Ben next to me.",  # From article 1
        "I mixed them. Orange! I painted a big round sun.",  # From article 2
        "Mia painted a tree. 'Look, birds!' she said. She added little brown dots.",  # From article 2
        "I made four little legs. My dog needed a head. I pinched some clay for ears.",  # From article 3
        "I used a stick to make eyes for my dog. Dot, dot! Mrs. Bell baked them in a special oven.",  # From article 3
        "I drew a black sky. I used my finger to smudge it. Soft!",  # From article 4
        "Sara drew a bat. It had pointy wings. 'Spooky!' I said.",  # From article 4
        "I found a picture of a dog. Cut! I glued it on my paper.",  # From article 5
        "Mrs. Bell said, 'Use your imagination!' I added a big purple butterfly."  # From article 5
    ],
    'sports day': [
        "I ran fast! My feet pounded the ground. Ben was next to me.",  # From article 1
        "I pushed harder. I crossed the line first! 'Yes!' I yelled.",  # From article 1
        "Sam got the ball next. He ran fast. I tried to stop him. Too late!",  # From article 2
        "I passed to Mia. She kicked hard. Goal! The whistle blew. 'Blue team wins!'",  # From article 2
        "The egg wobbled. Oh no! I slowed down. Ben passed me.",  # From article 3
        "I stopped. Took a breath. Then I walked slow and steady.",  # From article 3
        "My feet dug into the grass. The other team pulled back. The rope moved.",  # From article 4
        "We pulled harder! The rope moved our way. A little more. Then a lot!",  # From article 4
        "I ran fast down the path. Jump! I flew through the air. Then I landed in the sand. Thump!",  # From article 5
        "I tried again. Run, run, jump! I landed hard. Sand flew. 'Two meters five!' Better!"  # From article 5
    ],
    # 朋友互动类
    'park play': [
        "I pushed her back. Higher! She went up high. 'Whee!'",  # From article 1
        "We ran to the slide. Climb up fast. Whee down! Ben won.",  # From article 1
        "Ben ran fast around the big tree. I almost got him! He dodged away.",  # From article 2
        "Sara screamed and ran. She climbed up the slide. Safe! Ben couldn't tag her there.",  # From article 2
        "The ladybug crawled on my finger. Tickly! It flew away.",  # From article 3
        "Then we picked dandelions. Puff! We blew the white fluff. Make a wish!",  # From article 3
        "'Find treasure!' said Tom. We dug and dug. My hands got sandy.",  # From article 4
        "Then we built a castle. Walls and towers. We used sticks for flags.",  # From article 4
        "I slipped! Fell on my knee. Ouch. Ben ran over. 'Are you okay?' he asked.",  # From article 5
        "We sat on a bench. Watched other kids play. My knee felt better soon."  # From article 5
    ],
    'secret game': [
        "My Friend Whispers Behind the Wall",
        "We crawled under the branches. It was shady inside. 'Shh, secret meeting!' Leo said.",  # From article 1
        "We made a password. 'Banana bread!' Sara laughed. 'That's silly!'",  # From article 1
        "I heard Ben. 'Ready or not!' Footsteps. He looked in the kitchen. Not there!",  # From article 2
        "He opened the door! 'Found you!' he yelled. I jumped. 'Good hiding spot,' Ben said.",  # From article 2
        "Leo passed me one. It had shapes! Circle, square, triangle.",  # From article 3
        "Sara didn't know the code. 'What does this say?' she asked. We wouldn't tell.",  # From article 3
        "The path ended at a small stream. 'Our secret place,' Tom said.",  # From article 4
        "A frog jumped! We stayed very still. 'This is our spot,' I said.",  # From article 4
        "We 'hid' behind a tree. Peeked out. Mr. Jones put mail in a box.",  # From article 5
        "Mrs. Smith was gardening. 'Suspect watering flowers,' I whispered. We took notes in a little book."  # From article 5
    ],
    'tree house': [
        "Hammer and nails. Bang, bang! 'Hold this board,' Dad said.",  # From article 1
        "We put a rope ladder. Climb up, up. Inside, we put a small rug. 'Our secret base!' Ben said.",  # From article 1
        "Pitter-patter on the roof. Me and Sara played cards. 'Go fish!' she said.",  # From article 2
        "We told stories. Scary ones! The wind blew. The tree house creaked. 'Ooooh, ghosts!' I said.",  # From article 2
        "'Rule one: No girls allowed!' Ben nodded. 'Except Sara,' he said.",  # From article 3
        "We signed our names. Then we ate cookies. Crumbs everywhere! 'We need a broom,' Ben said.",  # From article 3
        "Flashlights. 'Spooky stories!' said Leo. He told one about a big bear.",  # From article 4
        "We heard noises. Owls? 'Hoo, hoo!' Rustling leaves. 'Just the wind,' Leo said.",  # From article 4
        "We got brushes. Climbed up. Paint the walls! Blue dripped down. Oops.",  # From article 5
        "We were tired. But it looked great. Our blue and red tree house. Shiny and new."  # From article 5
    ],
    'bike ride': [
        "As we walk, the wind carries us forward, pushing us toward the center of the road.",
        "Wind in my face! Fast. 'Race you to the corner!' Ben yelled.",  # From article 1
        "We pedaled hard. My legs worked fast. Ben was ahead. I pushed harder.",  # From article 1
        "I knew a shortcut. Through the alley. Bumpity-bump on the stones.",  # From article 2
        "After playing, we rode back. Tired legs. 'Ice cream stop?' Ben asked.",  # From article 2
        "Splash through puddles! Water sprayed up. 'Wet socks!' Leo laughed.",  # From article 3
        "We rode around the block. Again and again. Big splashes. Laughing hard.",  # From article 3
        "Greasy and black. 'Need help?' asked Tom. He rode up. 'I know how,' he said.",  # From article 4
        "He put it back on the gear. 'Try now.' I pedaled. It worked!",  # From article 4
        "Down the quiet street. Past houses with lights on. 'Smell that?' Mia said.",  # From article 5
        "We rode to the hilltop. Watched the sun go down. Into the water! Gone."  # From article 5
    ],
    'rainy game': [
        "I climbed a ladder. Ben slid down a snake. 'Oh no!' he groaned.",  # From article 1
        "Then we played cards. Go fish! 'Got any threes?' Ben asked. 'Go fish!' I said.",  # From article 1
        "We took flashlights. Made shadow puppets. Dog! Rabbit! 'Look, a monster!' I made big hands.",  # From article 2
        "We told stories. Silly ones. Ate cookies in the fort. Crumbs everywhere!",  # From article 2
        "We looked for straight pieces. Blue sky pieces. Green grass.",  # From article 3
        "Slowly, the picture came. A farm! Cow, barn, tractor. 'I found the cow's head!' I said.",  # From article 3
        "We acted out stories. Rescue the princess! Chase the bad guy!",  # From article 4
        "So we sat down. Had a tea party. With real juice! 'Fancy tea, princess?' I asked Sara.",  # From article 4
        "Cracked an egg. Stirred and stirred. 'Chocolate chips!' said Ben. We poured in lots.",  # From article 5
        "We watched them bake. Got bigger! Ding! Cookies done. We waited for them to cool."  # From article 5
    ],
    # 自然探索类
    'garden find': [
        "I had a small shovel. Dig, dig! I found a worm! Long and pink. It wiggled.",  # From article 1
        "I found a smooth white rock. Treasure! I washed it. Put it on my shelf.",  # From article 1
        "Sara had a net. 'There!' she whispered. A yellow one! She swung the net.",  # From article 2
        "A small white butterfly came close. It landed! On a daisy.",  # From article 2
        "'See the beans?' he said. Green beans hanging down. 'Pick some,' he said.",  # From article 3
        "Grandpa opened one. Little green peas inside. 'Try one,' he said.",  # From article 3
        "Every day I checked. Nothing. Then one day... green shoot! Tiny leaves.",  # From article 4
        "It grew taller. And taller! Big leaves. Then a bud. Yellow petals opened.",  # From article 4
        "Under a log. Centipede! Lots of legs. Fast. 'Don't touch,' said Mom.",  # From article 5
        "We found a spider web. Dew drops on it. Shiny like jewels."  # From article 5
    ],
    'beach day': [
        "We dug a big hole. Water filled it. Our moat! We piled sand high.",  # From article 1
        "A wave came. Splash! Our moat got bigger. Another wave. Oh no! Castle washed away.",  # From article 1
        "'A whole one!' I found a perfect spiral shell. Put it in my bucket.",  # From article 2
        "We dug in the wet sand. Found clams! Little ones. They squirted water when we touched them.",  # From article 2
        "Wind was strong. Dad held the string. I ran with the kite. Up it went!",  # From article 3
        "Red and blue in the sky. 'Higher!' I yelled. It danced. Pulled hard.",  # From article 3
        "I ran! Jumped on the board. Whoosh! Rode the wave to the sand. Fun!",  # From article 4
        "I did it again. And again. Salt water in my mouth. Yuck! But fun.",  # From article 4
        "We sat on towels. Ate sandwiches. Sand in my food? Crunch! We didn't mind.",  # From article 5
        "Watched the sun go down. Into the water! Gone. Stars came out. Bright."  # From article 5
    ],
    'forest walk': [
        "'Look!' said Mom. A deer! It stood still. Looked at us. Brown eyes.",  # From article 1
        "Then ran away. Quiet. We heard birds. Tweet, tweet! Squirrels ran up trees.",  # From article 1
        "Water bubbled over rocks. Clear! I saw a fish. Small and silver.",  # From article 2
        "We skipped stones. Flat ones. One, two, three skips! Good.",  # From article 2
        "Not to eat. Just to see. We found red ones with white dots. Like in books!",  # From article 3
        "Brown mushrooms under a log. Slimy. Big white ones. Like umbrellas.",  # From article 3
        "We ate our lunch. Sandwiches taste better outside. Ants found our crumbs.",  # From article 4
        "Tiny workers. We packed up. Left no trash. Good hikers.",  # From article 4
        "In the mud by the stream. 'Deer,' said Dad. Hoof prints. Then smaller ones.",  # From article 5
        "Saw a hole under a tree root. 'Rabbit home?' I whispered."  # From article 5
    ],
    'firefly night': [
        "Tiny lights in the yard. Blink. Blink. Like stars on earth.",  # From article 1
        "I ran gently. Cupped my hands. Caught one! Soft light in my hands.",  # From article 1
        "Fireflies everywhere! In the bushes. Over the grass. 'Count them!' said Dad.",  # From article 2
        "We turned off the porch light. Darker now. More fireflies! A light show just for us.",  # From article 2
        "Ran across the lawn. Jumped to catch one. Missed! They flew higher.",  # From article 3
        "A firefly landed on my knee! Glowed for a second. Then flew off.",  # From article 3
        "Caught a few in a jar. Put it on the table. Our night light!",  # From article 4
        "After dessert, we let them go. They flew into the dark. Little lights disappearing.",  # From article 4
        "Dozen s! Like fairy lights. We lay and watched. 'Make a wish on a firefly,' Sara said.",  # From article 5
        "We fell asleep watching the blinks. Sweet dreams."  # From article 5
    ],
    'snow play': [
        "White and soft. 'Build a snowman!' I yelled. We rolled big balls.",  # From article 1
        "We made snow angels next. Lie down. Move arms and legs. Up! Angel shape.",  # From article 1
        "Me against Ben and Sara. I built a wall. Snow bricks! Peeked over.",  # From article 2
        "Ben packed his own snowballs. Fast! Threw one. Hit Ben's leg. 'Got you!'",  # From article 2
        "I sat on my red sled. Pushed off. Whoosh! Wind in my face. Down, down! Bump!",  # From article 3
        "I pulled my sled back up. Hard work. Worth it. Down again! Faster this time.",  # From article 3
        "Little paw prints. 'Rabbit?' I said. We followed them. Into the bushes.",  # From article 4
        "Bigger prints. 'Deer!' said Dad. Hoof marks. We saw the deer far away.",  # From article 4
        "Inside! Warm house. Took off wet clothes. Cozy socks. Mom made cocoa.",  # From article 5
        "Marshmallows on top! Drank it. Warm in my tummy."  # From article 5
    ],
    # 日常小事类
    'helping mom': [
        "Socks first! Find pairs. Roll them up. Easy. Then shirts. Mom showed me how.",  # From article 1
        "Fold arms in. Then fold in half. I tried. A bit messy. 'Good try,' Mom said.",  # From article 1
        "I washed the wheels. Dirty! Mud came off. Then the doors. I drew a smiley face with soap.",  # From article 2
        "Rinsed with the hose. Spray! Water everywhere. I got wet. Shiny clean car.",  # From article 2
        "'Get apples,' Mom said. I picked red ones. Shiny. Then cereal. My favorite kind!",  # From article 3
        "At checkout, I put things on the belt. Beep, beep! The lady scanned.",  # From article 3
        "Added chocolate chips. Lots! Spooned dough on the tray. Mom put it in the oven.",  # From article 4
        "Smell filled the kitchen. Yum! Ding! Cookies done. We waited. Ate warm cookies.",  # From article 4
        "I put cars in their box. Books on the shelf. Dirty clothes in the basket.",  # From article 5
        "Made my bed. Pulled the blanket smooth. Mom vacuumed. Whirr! Room looked great."  # From article 5
    ],
    'pet care': [
        "I shook the food bottle. Tap, tap! Goldie swam up. I sprinkled little bits.",  # From article 1
        "She ate them fast. Gulp, gulp! Then I cleaned her bowl. Carefully!",  # From article 1
        "Put on his leash. 'Walk time!' He wagged his tail. Fast! We went to the park.",  # From article 2
        "Buddy sniffed everything. Trees. Poles. Mailboxes. He peed a lot!",  # From article 2
        "She purred. Loud! I used the soft brush. Stroked her back. Fluffy fur.",  # From article 3
        "Hair came off. Made a little fur ball. Mittens liked it. She rubbed my leg.",  # From article 3
        "Buddy's bowl was big. Water splashed. Mittens drank daintily. Lick, lick.",  # From article 4
        "Goldie just swam. All happy. Pets need water.",  # From article 4
        "Threw his ball. 'Get it!' He ran fast. Grabbed the ball. Ran back.",  # From article 5
        "Dropped it at my feet. 'Good boy!' I threw it again. And again."  # From article 5
    ],
    'baking day': [
        "My heart raced as I realized what this paper could be used for.",
        "I helped knead. Push, fold, push! Dough got smooth. We let it rest.",  # From article 1
        "It grew bigger! Poked it. Bounced back. Put it in a pan. Into the oven.",  # From article 1
        "I made frosting. Pink! With sprinkles. Cupcakes cooled. I frosted them.",  # From article 2
        "Swirls! Added sprinkles. Pretty. Tasted one. Sweet! Party will be fun.",  # From article 2
        "I spread tomato sauce. Then cheese. Lots! Pepperoni slices.",  # From article 3
        "I made a smiley face. Mom put it in the oven. Cheese bubbled. Smelled cheesy.",  # From article 3
        "We put apples in. Covered with top crust. Pinched edges. Fork holes.",  # From article 4
        "Into the oven. Apple smell filled the house. Warm and sweet.",  # From article 4
        "Rolled the dough. Used cookie cutters. Stars! Hearts! Trees! Baked them.",  # From article 5
        "Then we iced them. Red, green, blue. Sprinkles! Messy fun."  # From article 5
    ],
    'library visit': [
        "I looked for dinosaur books. Found one! Big pictures. Sharp teeth. Then a space book.",  # From article 1
        "I sat at a small table. Read about Mars. Red planet. Quiet in the library. Shhh!",  # From article 1
        "Big voice! She showed pictures. Kids sat on the rug. I listened.",  # From article 2
        "Dragon lost his fire! Oh no. Found it again. Happy ending. We clapped.",  # From article 2
        "'Now you can borrow books,' the lady said. I chose two. One about trucks. One about the ocean.",  # From article 3
        "She scanned my card. Beep! 'Bring back in two weeks,' she said. I held my books tight.",  # From article 3
        "Looked up books about dogs. I typed 'dog'. Many books! I wrote down numbers.",  # From article 4
        "Found the shelf. Looked. Found one! Big dogs, small dogs. Pictures. Sat on a beanbag.",  # From article 4
        "Big puzzle! 500 pieces. Sky and clouds. I helped. Found blue pieces.",  # From article 5
        "Others helped too. Slowly, picture grew. Almost done! Missing one piece."  # From article 5
        "I walked over to the children's section. I picked one with animals on the cover.",
        "I started to read it right away. Every page got funnier.",
        "I asked the nice lady for help. She showed me a big book with pictures.",
        "He picks one up. 'Ah, I know this story!' he says.",
        "I sat right down on the floor. Each page showed stars and planets."
    ],
    'bedtime fear': [
        "I called, 'Mom!' She came in. 'What's wrong?' she asked. 'Shadows look scary,' I said.",  # From article 1
        "She turned on the small light. Soft glow. 'See? Just your chair,' she said.",  # From article 1
        "I hid under my blanket. Scared. Dad came in. 'Big storm,' he said. He sat with me.",  # From article 2
        "'Thunder is just clouds bumping,' he said. Lightning flashed. 'Count!' he said. 'One, two...'",  # From article 2
        "Woke up scared. Heart beating fast. Went to Mom's room. 'Bad dream,' I whispered.",  # From article 3
        "She hugged me. 'Not real,' she said. She walked me back to bed. Tucked me in.",  # From article 3
        "I heard a noise! Tap, tap. On the window. 'Mom!' I called. She came. 'What is it?'",  # From article 4
        "'A noise!' I said. She listened. Tap, tap. 'Just a branch,' she said.",  # From article 4
        "Under the bed? I looked. Dark! Dad came. He looked under. 'No monsters,' he said.",  # From article 5
        "He gave me a small flashlight. 'Use this if scared,' he said. I held it. Felt brave."  # From article 5
    ]
}

NARRATIVE_EXAMPLES2K = {
    'magic garden': [
        "Pushing through the leafy curtain, I entered a glowing garden where purple flowers pulsed with soft light.",
        "She showed me miniature houses and berry snacks before sunset painted the sky.",
        "With careful tickling, I made the invaders leave and the grateful frog king gifted me dewdrop jewels that still sparkle on my windowsill.",
        "Nowadays we share weekly teatime beneath weeping willows, proving magic lives in ordinary places if we pay attention.",
        "So I crafted leaf umbrellas for their village and they repaid me with honey-sweet nectar.",
        "Though others doubt my story, my pockets still smell like sky blossoms, a secret comfort that stays with me through boring school days.",
        "We celebrated with a fruit drop feast beneath twinkling fireflies, and since then I leave breadcrumb gifts for them nightly.",
        "Their tiny thank-you notes written on petals remind me that secret friends make ordinary gardens magical.",
        "Inside, singing roots led me through emerald tunnels to a chamber filled with luminous trees.",
        "Grandma recognized it immediately as her own childhood discovery, some garden mysteries passing through generations and binding family stories with the land's magic."
    ],
    
    'beach treasure': [
        "Digging frantically, my fingers scraped a rusty metal box filled with ancient coins and a faded map.",
        "Inside glimmered silver coins and a pearl necklace tangled like sea stars, while the waves crashed approval and seagulls circled overhead.",
        "More digging uncovered a corroded chain bearing a heart-shaped locket with a photo of a smiling woman and the inscription 'To my darling, summer 1949'.",
        "After weeks of research, we returned it to Martha Jenkins, who tearfully recalled losing it during a hurricane evacuation fifty years prior, her stories painting vivid pictures of beach life gone by.",
        "Crafting a driftwood treasure chest, I reburied them deliberately and watched a little boy dance joyfully after discovering one, his excitement surpassing any personal gain.",
        "Our afternoon search yielded only sea-polished rocks, but those messages from Captain Wills fueled our imagination for weeks, their ghostly words teaching us that stories outlast all material treasures.",
        "Over lemonade, she recounted beach romance tales under wartime skies - memories brighter than any gem, teaching me treasures aren't always buried; sometimes they fly on wings waiting to be returned.",
        "That perfect day proved celebrations needn't be expensive - just intentionally joyful and shared with beloved people.",
        "My birthday culminated in releasing twenty beauties into Grandma's garden, showing that true gifts spark lifelong passions for life's winged wonders.",
        "This public artwork birthday honors still brightens Main Street - my permanent gift back to the community I love."
    ],
    
    'puppy rescue': [
        "Wrapping him in my sweatshirt, I carried the trembling bundle home and we towel-dried his matted fur while he licked our hands gratefully.",
        "Weeks later, Mr. Henderson claimed Bolt, his hearing-impaired terrier escaped during the storm, and seeing them reunite cemented my commitment to helping animals.",
        "Home warmth revived him gradually: warm rice-sock bed, gentle paw massages, nourishing broth, and social media shares eventually connected him to Maya, whose family had lost him during relocation chaos.",
        "Despite his pain, he licked my cheek gratefully as we rode carefully to the vet, who set his fracture gently and praised 'You saved this little life', showing me how to administer pain medication.",
        "We carried them home wrapped in towels, their tiny bodies shaking with cold, and creating a blanket nest, we offered warm milk through eyedroppers.",
        "Though fleeting companions, those helpless pups ignited my lifelong passion for animal welfare.",
        "Home warmth and chicken broth revived him visibly, and posters around the neighborhood worked - Mrs. Miller recognized her escaped Max!",
        "The reward money donated to shelters closed this circle of compassion that started with listening amidst fallen leaves."
    ],
    
    'rainy adventure': [
        "Giant sidewalk lakes swallowed my leaf boat flotilla, inspiring dam-building with sticks and stones, and 'Emergency worm rescue!' became our mission when displaced earthworms surfaced.",
        "We redirected water flows through sandbox canyons until drenched clothes forced retreat, and hot chocolate never tasted sweeter than after watery adventures.",
        "Rescuing them with branch hooks became serious business, and raindrops kissed our faces while we engineered canals connecting mud pools.",
        "Drawing cloud portraits in wet dirt, we imagined rain spirits painting skies until twilight painted wet streets gold, muddy boots marking triumphant paths home.",
        "'Splash contest!' Leo shouted, our synchronized jumps spraying fountains that soaked us shivering, and discovering tadpole clusters in tire tracks changed our mission to 'Protect the nursery!'",
        "We built rock walls shielding them from predators, and sudden sunshine birthed a double rainbow that led us chasing colors across fields.",
        "Near school bushes, faint mewing revealed a drenched kitten, and offering shelter in my hoodie pocket, we completed our journey dripping but united.",
        "Mrs. Gomez recognized the lost 'Drizzle', rewarding us with dry towels and cookies, and now Drizzle greets me rain or shine - proof that storms sometimes deliver blessings."
    ],
    
    "grandpa's story": [
        "His fingers traced young soldiers' faces while describing frozen Belgian forests where enemy planes sounded like angry bees, and he detailed sharing precious chocolate with local children despite rationing.",
        "When tears surfaced describing liberated concentration camps, I squeezed his hand gently, and our ritual singing of 'We'll Meet Again' transformed dates and names into living courage lessons.",
        "Stories unfolded - muddy trenches, cold rations, homesick letters worn thin from rereading - and we spent hours locating their battle sites on maps, Grandpa tracing paths with trembling fingers.",
        "We created charcoal sketches based on his stories - soldiers sharing canned peaches with starved children - and Grandpa said 'Memories need keeping,' tucking our drawings into the album.",
        "Over lemonade, she recounted beach romance tales under wartime skies, teaching me that true gifts spark lifelong passions.",
        "Faded letters revealed their courtship between battles, and Grandpa sighed 'War steals time,' but Mom gifted me Grandma's locket, and Grandpa smiled saying 'Guard love stories, kid - they make peace matter.'",
        "He demonstrated Victory Garden planting techniques used during rationing - making every inch fertile - and explained 'Duty isn't just fighting, but nurturing life.'",
        "Now our community garden stands where veterans teach kids cultivation - Grandpa's quiet legacy rooting hope in soil."
    ],
    
    'treehouse secret': [
        "Prying them up revealed a dusty tin box filled with vintage marbles, faded comics, and a 1958 note: 'For fellow climbers - share the magic.'",
        "Inspired, we added our Pokémon cards and friendship bracelets, burying it deeper for future explorers, transforming our perch into a timeless treasure trove accessible only with the special knock.",
        "Peering through, I discovered an invisible hawk's nest across the valley, and following handwritten instructions inside its case, I mapped local bird territories daily.",
        "This secret legacy sparked my passion for ornithology - teaching that wonder often hides in overlooked corners.",
        "Digging there unearthed a glass jar containing their childhood diary pages and crayon drawings!",
        "We added contemporary comics before reburying their time capsule, creating a generations-long friendship across decades by writing yearly letters to future finders.",
        "We added LEGO figures and buried new treasures at the map coordinates provided, discovering that earlier kids had created neighborhood scavenger hunts.",
        "This game with unseen 'tree spirits' fosters imagination while teaching that wonder requires no proof, only participation."
    ],
    
    'lost kitten': [
        "'Easy now,' I soothed while extracting the drenched creature, and home warmth and eyedropper feedings gradually revived her.",
        "Weeks later, Mitzi recognizes my bike bell, scampers for chin rubs, while Mrs. Peabody's oatmeal cookies prove kindness boomerangs beautifully.",
        "Patient tuna offerings finally coaxed out a shivering calico, and 'You're safe now,' I whispered while drying her delicate fur.",
        "Their tearful reunion - his first wife's namesake cat - cemented that saving lives sometimes means bridging distances between neighbors who become friends.",
        "Teachers helped gently free the frightened baby while he licked our fingers gratefully, and 'No chip means he's yours!' smiled the shelter worker after scanning.",
        "Now Scout follows me everywhere, his rescue anniversary marked with tuna cakes and neighborhood education about microchipping pets properly.",
        "Months of patience earned trust; she now sleeps curled on my pillow, demonstrating how rescuing animals often means healing ourselves through steady care.",
        "The shelter identified her microchip owner - Mrs. Rivers hospitalized suddenly - and 'You saved my baby!' she wept upon recovery."
    ],
    
    'cookie mystery': [
        "Setting honey traps - fresh batches as bait - I photographed him red-pawed smuggling gingersnaps!",
        "'Convicted sweet tooth!' declared my trial presentation, and Judge Mom sentenced Max to cleanup duty during future baking sessions, securing our cookie jar on the fridge.",
        "His tearful confession - he'd shared them with his teddy bear - inspired collaboration; we measured ingredients together, Charlie proudly cracking eggs.",
        "Those shared cookies tasted sweeter, proving that cooking together repairs more than just snack shortages.",
        "Creating a dedicated 'critter cookie' station outdoors using nutty biscuits solved pantry raids, and now squirrels perform circus antics for their treats while we enjoy crumb-free cookies indoors.",
        "We created signature recipes - 'Lunar Lemon Drops' and 'Starry Shortbread' - these secret baking sessions forging sisterhood sweeter than any stolen treat."
    ],
    
    'camping surprise': [
        "Dad's headlamp revealed raccoon twins systematically unpacking our cooler, laughing as they unlatched locks, popped containers, and devoured sandwich meats with expert precision.",
        "Gentle broom-waving shooed them off, though mama raccoon escaped with a whole hotdog pack, and Ranger Joe later explained their generations-old campground expertise.",
        "Unzipping carefully, we discovered an owl perched silently nearby, and Mom whispered 'Night guardian' as it swiveled its head almost completely around.",
        "Watching it glide soundlessly on shadow wings reshaped my understanding of nighttime wonders, inspiring our annual owl-calling contests back home.",
        "Swinging my flashlight revealed a whole deer family with glowing eyes, and motionless minutes passed as we stared at each other until they bounded away gracefully.",
        "That breathtaking encounter fuels my wildlife photography today - every shutter click chasing that first gasp of wildness.",
        "Peeking outside, we discovered wind rolling pinecones against our shelter like nature's bowling balls, and their rhythmic strikes became comforting white noise as we named players: 'Big Roller' versus 'Speedy'.",
        "Our relieved high-fives celebrated crisis avoidance - and reinforced leaving NO trace campsites thereafter, making that aromatic near-disaster our funniest family camping legend."
    ],
    
    'birthday magic': [
        "An elaborate hunt ensued: deciphering kitchen cupboard notes, measuring backyard sundial angles, finally digging beneath the oak's 'X', and burlap wrappings hid access ladders to my newly built 'Sky Castle' treehouse!",
        "Friends cheered below as I raised our Jolly Roger flag, cementing this sky-high sanctuary for midnight adventures.",
        "Talent show night, I stunned classmates producing twenty-five scarves from one tube, transforming nervous shakes into proud confidence and fueling my hospital magic volunteer work.",
        "Sunset brought dolphin-watching as waves sang 'Happy Birthday', proving celebrations needn't be expensive - just intentionally joyful.",
        "We watched tiny jaws munch leaves, spun chrysalises emerge miraculously into painted lady butterflies, and my birthday culminated in releasing twenty beauties into Grandma's garden.",
        "This public artwork birthday honor still brightens Main Street, serving as my permanent gift back to the community."
    ],
    
    'library ghost': [
        "Opening it revealed caretaker ghost Elara's legend: punishing book vandals but helping truth-seekers, and pencil margin notes in nearby poetry books glowed neon blue pointing to brick irregularities.",
        "Librarian Ms. Chen helped excavate Elara's Victorian-era walled-up study, and her preserved journals now feature in local history tours - ghosts guiding remembrance.",
        "Placing marigolds on her former desk brought subtle lavender scents next visit, and now fresh flowers appear regularly beside forgotten children's classics.",
        "Nowadays, fresh flowers appear beside restored books, a silent thanks for remembrance.",
        "Whispering 'Need help?' received book spine taps directing me to overlooked city planning documents proving park preservation claims.",
        "These fragile vessels now anchor community memorials, reminding residents that every era's dreams deserve remembrance.",
        "Displaying it respectfully stopped disturbances immediately, and the ghost girl's unfinished math problems now feature in our intergenerational tutoring project.",
        "This spectral tutoring relationship continues - my geology award dedicated to 'Miss Lily: Phantom Professor Extraordinaire'."
    ],
    
    'snow friend': [
        "With carrot noses and charcoal eyes, Frosty grew stick arms reaching for clouds, and soon neighbors expanded our family: Mrs. Miller knitted mittens, the Parkers added pinecone pets.",
        "Our snow-sculpture block parties featured ice turrets and frozen fountains - transient art connecting neighborhoods.",
        "Our class constructed elaborate Arctic kingdoms with ice bridges spanning snow rivers, and 'Best snow day ever!' echoed as we tunneled through drifts towards candy castle spires.",
        "When thaw threatened destruction, we launched epic snowball siege wars that ended in rosy-cheeked cocoa truces.",
        "Our team sculpted Olympic-quality bobsled tracks polished by repeated runs, and we proclaimed 'Record holders!' timing daring descents until sunset painted snow pink.",
        "Cold fingers warmed around bonfires roasting marshmallows while snow sculptures glowed beneath holiday lights, continuing this frozen sportsmanship tournament annually.",
        "We built rock walls shielding them from predators, and sudden sunshine birthed a double rainbow that led us chasing colors across fields.",
        "Imagination transformed fleeting ice into lasting neighborhood legends by assigning snowmen personas like Pirate Pete guarding buried treasure or Miss Snowflake teaching ice-science."
    ],
    
    'frog prince': [
        "'Your Highness!' I declared, crafting reed crowns, and next evening a boy named Liam appeared claiming my kiss transformed him.",
        "Weeks passed rescuing tadpoles, building lily pad rafts until autumn winds dissolved our fantasy, leaving cherished memories proving shared imagination conjures real magic.",
        "Our 'Frog Royalty Project' installed turtle-safe pond ramps and chemical-free zones, and today thriving amphibian populations prove environmental guardianship creates truer transformations.",
        "Biologists visited, explaining amphibian skin sensitivities, safely redirecting enthusiasm into our 'Frog Friendly Habitat' receiving conservation awards.",
        "Recording nocturnal croaks decoded surprising communication patterns, and our illustrated 'Frog Kingdom Chronicles' detailed predator warnings and mating calls, winning science prizes.",
        "Imaginary royalty became genuine scientific discovery - curiosity opening doors to nature's authentic marvels.",
        "We stage 'Pond Kingdoms' plays starring local amphibians through telescopes annually, proving that shared performances build community bridges stronger than any magic kiss."
    ],
    
    'broken wing': [
        "Grandma's teacup became its sanctuary, soft cloths cushioning delicate bones, and wildlife experts guided us through eyedropper feeds.",
        "Releasing 'Sparrow' felt bittersweet - she lingered on our swing-set singing briefly before vanishing skyward, inspiring bird feeders bearing her painted portrait.",
        "Warm rice-sock bed revived it while we learned specialized feeding techniques, and release day brought circling parents reclaiming their baby - family reunions proving nature heals best.",
        "Their recognition honors that cross-species friendships transform both rescuers and rescued.",
        "Professional rehabbers taught us proper handling during convalescence, and patience won trust despite 'Skye's' eagle-keen gaze.",
        "That magical moment releasing her still inspires my dream of becoming a wildlife veterinarian.",
        "Creating a makeshift nest, we guarded it until rescue arrived, and weeks later a school visit featured our owl - newly flighted!",
        "Seeing children gasp in wonder reinforced that every rescue radiates education, connecting communities to nature."
    ],
    
    'midnight snack': [
        "Tiptoeing past parental snores, I avoided toy landmines successfully, and fridge light revealed leftover birthday cupcakes.",
        "But crinkling frosting wrappers betrayed me - parental flashlights pinned me, sparking impromptu floor picnics under moonlight.",
        "Whispering 'Raid Team Assemble!' my sister and I navigated squeaky floors stealthily, securing cheese blocks and apple slices for feasts beneath blanket forts.",
        "Parental discoveries ended with milk-and-story truces, forging sibling solidarity sweeter than treats.",
        "Discovering pudding cups became celebratory rituals marked by window-seat banquets during full moons.",
        "After scary nightmares, stealthy kitchen visits soothed nerves, and warm milk sipped slowly beneath nightlights transformed fears into comfort.",
        "Discovering foreign leftovers became international culinary adventures under flashlight beams, sampling Korean kimchi or Italian olives.",
        "Now families exchange 'Midnight Munchies Boxes' during cultural festivals - subterranean tastings bridging traditions."
    ],
    
    'message bottle': [
        "Online translators helped craft responses featuring English class photos and pressed wildflowers, and Monica's reply began correspondence spanning cherry blossoms versus sardine festivals.",
        "Months later, her family visited bearing custard tarts, proving oceans don't separate kindred spirits.",
        "'Future finder: be curious!' my message urged beside friendship bracelets, and years later Canadian fisher-boy Jason discovered it.",
        "The simple bottle taught that hope cast upon waters returns manifold.",
        "We established local history projects honoring senders, displaying bottles beside digital biographies.",
        "They sent conservation toolkits inspiring school eco-projects, proving environmental action starts with casting hope outwardly.",
        "Years later, bedridden poet Mrs. Arden received one, her joyous response detailing its impact during illness sparked collaborations.",
        "One floating verse created ripples healing writer and receiver simultaneously."
    ],
    
    'hidden cave': [
        "Pushing through green curtains, our headlamps revealed walls sparkling with crystal teeth and deeper inside, bioluminescent algae painted everything sapphire blue - a living galaxy underfoot.",
        "Marine archaeologists later confirmed ship timber was from the 18th-century Spanish galleon 'Esperanza', our names gracing museum displays while the protected cave serves scientific research.",
        "Flashlights illuminated ancient fish drawings glowing with mineral pigments, and tribal historians identified them as lost Chumash navigation maps.",
        "Now elders lead moonlit tours telling creation stories, teaching me true discovery means returning treasures to rightful storytellers.",
        "Squeezing through, we entered cathedral-like caverns where waterfalls thundered through darkness, and glowing fungi lit albino insects dancing around underground rivers.",
        "Guided ecotours now fund conservation projects, proving youthful curiosity preserves nature responsibly.",
        "Quartz walls refracted our flashlight beams into rainbows, revealing giant bones in dusty alcoves, and paleontologists identified ground sloth fossils from the Ice Age.",
        "Conservationists identified endangered Townsend's big-eared bats roosting there, and we helped install infrared cameras monitoring colonies without disturbance."
    ],
    'parade float': [
        "Riding inside crepe paper flames, I waved as confetti 'fireworks' exploded overhead.",
        "Winning 'Most Innovative' brought community donations funding space camps, and now annually we design new celestial floats - proving glitter and glue can launch lifelong dreams.",
        "Rescue dogs wore seaweed costumes while 'Save Nemo' signs urged adoption during our cheerful spectacle that found homes for 43 animals!",
        "Humane society partnerships now make this a yearly tradition - turning celebration into life-saving advocacy through wagging tails and happy endings.",
        "Farmers donated produce we sculpted into edible art, and after the parade, volunteers transformed it into 200 community meals.",
        "This shared sustenance tradition teaches that art nourishes both spirit and body - creativity blossoming from soil to soup pot.",
        "Children crafted miniature cultural costumes while elders shared traditions during our 'Dollhouse of Nations' float.",
        "Parade prizes funded language classes where we now learn Mandarin songs and Mexican folk dances, proving those dancing dolls built bridges stronger than any politician's speech.",
        "Our 'Rainbow Connection' float toured streets spreading chalk-drawn joy while neighbors left treat bags on porches and local businesses sponsored prize packs.",
        "This reinvented celebration proved community spirit finds pathways even through closed doors - hope rolling on bicycle wheels."
    ],
    
    'magic paint': [
        "Mixing science and art, constellations glowed where hands touched walls - meteors streaking across imagined galaxies in our phosphorescent-painted garage cosmos.",
        "City arts grants now fund downtown murals where alleyways bloom with community creativity - proving magic lives in shared imagination.",
        "Community volunteers maintain seasonal transformations where painted seahorses 'swim' via stop-motion tricks - winter ice castles becoming spring tulip fields.",
        "This living canvas proves public spaces become wondrous when collective dreams paint outside the lines.",
        "Children now hunt for painted secrets after school, transforming neglected alleys into sought-after wonderlands through perspective tricks creating 'hidden doors' revealing waterfalls cascading down brick walls.",
        "A simple brushstroke can redefine a neighborhood's story when dull fences disappear under fantasy landscapes.",
        "Elders described nostalgic scenes while teens painted vibrant interpretations, creating 'Memory Murals' that now adorn care facilities nationwide.",
        "Pigments and stories heal where words fail, especially when dementia patients trace familiar patterns with trembling fingers.",
        "Children 'plant' imaginary crops that 'grow' when rain falls on parking blocks transformed into miniature farms with water-reactive chalk.",
        "City planners adopted this 'Playable Streets' concept - proving creativity transforms mundane spaces into fields of possibility."
    ],
    
    'island quest': [
        "Free-diving located sunken WWII planes identified through naval archives, and marine archaeologists displayed our findings using innovative 3D mapping.",
        "This teenage adventure launched my ocean conservation career - proving youthful curiosity can surface forgotten histories.",
        "We documented colonial ship fragments unrecognized locally, and 'Junior Historian' awards funded archaeological surveys revealing 18th-century trade routes.",
        "Sometimes X marks cultural heritage more valuable than gold discovered during summer camp voyages that became treasure hunts with historical clues.",
        "Albatross tracking tags we placed revealed migration patterns assisting climate studies, transforming stargazing games into serious science contributions.",
        "What began as celestial navigation lessons to uncharted islands now drives vital ecological data collection.",
        "Discovering rare shellfish habitats added features to marine maps during youth regattas guided by star charts to hidden coves.",
        "Conservation awards proved adventure and stewardship sail together - each voyage writing new chapters in coastal protection.",
        "Finding replies from distant islands built pen-pal friendships across oceans through message bottles launched in poetic scavenger hunts.",
        "These floating letters foster cultural understanding where borders divide - bottled words building bridges."
    ],
    
    'circus mouse': [
        "His cheese-motivated tightrope walks earned standing ovations during 'Pip's Grand Circus' where we engineered obstacle courses from LEGO ramps and paper tunnels.",
        "Community performances now fund animal shelters - proving tiny feats inspire mighty compassion.",
        "Videos raised humane education funds while teaching respect for small lives through 'Miniscule Circus' exhibits observing rescued mice's natural agility.",
        "Even pocket-sized creatures deserve standing ovations when starring in educational dioramas.",
        "Students engineered stadiums where mice raced through mazes during classroom 'Rodent Olympics' demonstrating physics principles.",
        "Biology teachers integrated anatomy lessons into math challenges - proving play sparks interdisciplinary learning.",
        "Their imagined escapades entertained younger audiences while raising vermin control awareness through shadow puppet adventures inspired by escaped mice.",
        "Laughter disarms fear better than traps when mice inspire creative storytelling.",
        "Students built tiny 'circus bots' replicating natural movements through wood mouse observations guiding robotics design.",
        "These mechanical marvels demonstrate how nature guides engineering - whisker sensors outperforming digital designs."
    ],
    
    'sunflower giant': [
        "Pulley systems delivered us to cloud-level perspectives revealing neighborhood patterns when 'Big Sol' reached three stories high, shading our treehouse.",
        "Preserved stalks now host owl nests annually - life ascending skyward.",
        "Hollow stalks became natural treehouses for insect observation during backyard experiments growing record-breaking giants.",
        "Saved seeds now flourish in school gardens nationwide - proving small backyards can yield mighty science.",
        "Seasonal transformations hosted community concerts beneath golden canopies when sunflower tunnels arched over pathways like floral cathedrals.",
        "Environmental artists incorporated them into installations - nature's architecture inspiring human creativity.",
        "Garden clubs adapted trellis designs for urban farms after studying stalk structures modeling sustainable engineering.",
        "Sometimes the strongest blueprints grow from the earth.",
        "Elementary classes now cultivate generations of giants while stalks shelter winter wildlife from fading blooms gifting thousands of seeds.",
        "Endings sow new beginnings through continuous cycles of growth and renewal."
    ],
    
    'moon rabbit': [
        "Research journals correlating behavior with lunar cycles won science prizes - proving patience reveals nature's clockwork through full-moon photography capturing elusive hares' seasonal dances coinciding with berry harvests.",
        "Night cameras documented complex rabbit communications under moonlight, and published findings showed mythology often holds ecological truths.",
        "Companion planting techniques yielded chemical-free harvests through moon-phase gardening following rabbit populations.",
        "This natural partnership inspires regional farming revolutions.",
        "Stories about celestial messengers funded habitat conservation when children created rabbit folklore plays.",
        "Creativity rooted in reverence bears fruit through artistic expression.",
        "Their gentle presence comforts hospital patients while promoting adoption awareness through rescue rabbits becoming therapy companions.",
        "Compassion connects all species under the same moon."
    ],
    
    'robot friend': [
        "When school demos malfunctioned, classmates funded upgrades making him an educational ambassador whose janky movements charm students into coding careers.",
        "Student teams built park-cleaning bots and recycling sorters during cardboard robotics competitions solving community problems.",
        "Children reverse-engineered devices learning mechanics hands-on through repair workshops transforming broken toys into treasures.",
        "Sustainable skills grow from taking things apart and rebuilding.",
        "Programmed arms now help disabled neighbors pour tea through simple coding repurposing old robots.",
        "Technology serves best when extending human capability.",
        "Community centers host monthly sessions where trash transforms into moving art through recycling drives supplying robot workshops.",
        "One generation's junk becomes another's wonder through creative reuse."
    ],
    
    'pirate map': [
        "'Time Capsule Hunters' projects now preserve neighborhood histories - proving buried stories outlast buried objects found through attic discoveries of 1930s treasure maps.",
        "Children created pirate maps marking beach clean-up sites during summer camp cartography challenges directing conservation.",
        "Grandparents hid 'loot' using nautical charts, teaching geography through chocolate coin quests during family reunions featuring generational treasure hunts.",
        "Laughter echoes through parks when learning becomes play.",
        "Clues based on archival photos taught town heritage while supporting shops during local businesses-sponsored historic scavenger hunts.",
        "'Captain Kidd's Trail' funds preservation societies through community engagement.",
        "Inclusive hunts accommodate all explorers through school projects creating braille treasure maps.",
        "True treasure is discovering shared adventure needs no sight."
    ]
}

NARRATIVE_EXAMPLES3K = {
    'bicycle trail adventure': [
        "My wheels splashed through muddy puddles from yesterday's rain.",
        "Riding up the big hill made my legs hurt but I kept pedaling.",
        "'Watch for that bump!' Dad shouted as we jumped over tree roots.",
        "After eating our sandwiches, we raced downhill feeling like birds.",
        "Grandpa held my hand going down saying, 'Balance is key!'",
        "Near sunset, we saw deer watching us ride past their home.",
        "Our bike tires hummed on the dirt path along the river.",
        "Mud splattered our shirts when we hit puddles on the ride back down.",
        "When we got to the big hill, Dad pushed our bikes from behind.",
        "Fixing a flat tire taught me patience after the ride down."
    ],
    
    'garden harvest day': [
        "We filled baskets with beans and carrots I'd planted last spring, and finding a giant pumpkin made us cheer.",
        "Dirt stuck under my nails as I pulled potatoes, and sweating in the garden feels good when you see results.",
        "Our basket filled quickly with shining vegetables, and 'Did you plant all this?' my neighbor asked through the fence.",
        "Carrots came out covered in dark dirt, and we ate corn for dinner that night as seeds became miracles.",
        "Our basket got heavy carrying it all inside, and dirt stayed on the floor despite Mom's rug during the peeling process.",
        "Peeling carrots felt like finding treasure after washing them for our family meal.",
        "My gloves got muddy reaching under broad leaves, and tomatoes stained our shirts bright red when they broke.",
        "One vine held thirty beans all in a row, and seed packets now seemed magical looking at these plants.",
        "Sweating in the garden made me appreciate farmers, and 'This tastes better than store food,' my friend said at the end.",
        "Harvest day meant hard work but fun, and Grandpa called 'Don't forget the zucchini!' from his chair."
    ],
    
    'sunday pancake breakfast': [
        "Three pancakes stuck together making a tall stack, and syrup dripped off the table onto our bench.",
        "Maple smells filled the kitchen making tummies growl, and we ate at the small table listening to morning birds.",
        "Our batter swirled in the hot pan making patterns, and 'Flip fast!' she laughed when one almost burned.",
        "Syrup made rivers across fluffy mountains on plates, and we ate at the kitchen table sharing family news.",
        "The pan hissed when batter hit hot grease, and syrup dripped down chins making us wipe constantly.",
        "Our stack fell over like a building in cartoons, and 'Best breakfast,' Grandpa smiled with sticky whiskers.",
        "Syrup spilled making rivers on wood patterns, and we learned fractions counting how many we each ate.",
        "Cleaning sticky syrup off chairs took effort, but breakfast time filled our hearts before our bellies.",
        "Flipping practice caused three bad pancakes first, and syrup spilled when I poured without asking help.",
        "We built a funny leaning stack on green plates, and eating at the little table felt special for a Sunday tradition."
    ],
    
    'library book mystery': [
        "The story worried me about a missing cat, and pictures showed places I knew near home, making me ask 'Is this clue true?'",
        "She helped search library records for the author, and under 'M' shelf we found hidden answers showing mysteries live between book covers.",
        "Finding answers became my mission, and behind the poetry shelf I discovered old photos that solved last summer's park mystery.",
        "Librarian Mrs. Jones found more clues online, and our research proved books hold more than stories sometimes.",
        "This mystery worried me all through dinner, and I returned to library after homework to find missing posters from ten years ago.",
        "Librarian said, 'These stories inspire curiosity,' and finding truth took bravery in the end.",
        "Red circles marked places around town, and finding clues became my afternoon mission with worry prompting me to call my best friend Josh.",
        "Together we checked each spot after school, and behind the grocery store we found a painted box proving books open real adventures.",
        "'Have you seen this?' I asked worried librarian, and she helped me find newspaper shelf for research to solve a three-year old mystery.",
        "Finding answers felt better than fiction, especially when reading became detective work on Wednesday."
    ],
    
    'family pizza night': [
        "Flour covered the kitchen counter like snow, and I spread tomato sauce making funny patterns with cheese mountains piled high on each slice.",
        "Eating at the long table got messy fun, and cheese strings stuck to chins making us laugh during Friday pizza night.",
        "Cheese flew through the air during sibling fight, and sauce splattered the oven door dramatically during our family cooking session.",
        "Finding pineapple in hair became surprise later, and cooking together beats any restaurant experience.",
        "Toppings became islands on red sauce sea, and oven light showed melting magic happening before slice cutting made crisp sounds we loved.",
        "Table talk turned loud sharing week stories, and eating family food fills more than stomachs on rainy nights.",
        "My job was sprinkling cheese mountain high, and oven timer pinged when golden crust formed ready for slice dividing causing voting on fairness.",
        "Extra toppings sat ready for hungry seconds, and kitchen cleanup taught cooperation lessons for young chefs.",
        "Toppings became geography lesson places, and 'Cheese seals everything,' he winked baking with oven heat warming the whole kitchen space.",
        "Table setting turned into decoration art, and pizza tastes better homemade always according to Grandpa."
    ],
    
    'rainy day fort': [
        "Blankets draped over kitchen chairs made walls, and pillow mountains softened the floor space while storm noises sounded far away now.",
        "Flashlight stories made spooky shadows dance, and building shelter created cozy world on a rainy day.",
        "Blankets covered couch cushions for cave, and pillow road connected rooms secretly making inside feel safe from weather outside.",
        "Rain beat loud roof rhythm songs, and imagination filled small space wonderfully during storm warnings after school.",
        "Pillows became walls against thunder booms, and inside felt like separate adventure world where storm winds howled but we drank pretend tea.",
        "Building started quietly then grew bigger, transforming a boring room into a fort on heavy rain days.",
        "Pillows fortified sofa corner defenses, and building shelter became family project with books read till storm passed.",
        "Safe small space calmed frightened dog too, proving that shelters can handle unexpected weather.",
        "Blankets transformed boring room magically, and pillow tunnels connected secret bases keeping hands busy from boredom.",
        "Inside stayed warm despite howling wind, and storm day turned favorite memory with dewy grass wonder."
    ],
    
    'school art project': [
        "I dipped my fat brush into yellow paint, splattering some on Jamie's table, and we mixed blues and yellows to make perfect green grass.",
        "We pinned our dripping papers on the drying line proudly, and cleanup was messy with colorful handprints everywhere after Mrs. Parker shouted encouragement.",
        "My brush slid blue paint across paper like ice skating making a river, and Eva added glitter making sparkly fish that changed plans.",
        "Drawing sun rays erased yesterday's test stress, and bright colors danced everywhere turning art into joyful expression.",
        "Paint drips became mountain tops accidentally, and when green splatted on my paper, we changed plans declaring 'Now it's a forest!'",
        "Brushes dipped made rainbow puddles everywhere, and color choices became serious business when deciding sky colors.",
        "We got so concentrated you could hear brushes swishing, and seeing our pictures displayed later felt like playtime triumph.",
        "Messy red spots decorated my jeans permanently, proving real art wears itself through happy accidents.",
        "Color flowed wherever our hands led with no rules, and we laughed making handprint rainbows during cleanup.",
        "This messy freedom taught me art isn't about perfect lines, but joyful hearts creating together in the classroom."
    ],
    
    'lemonade stand adventure': [
        "Lemons rolled everywhere as we squeezed pitchers full, and cups lined the wobbly table neatly with coin jar filling slowly.",
        "Selling to Mrs. Lee, I spilled cold lemonade on her shoes, and she laughed buying extra cups showing sticky business welcomes mistakes.",
        "Three lemons escaped to the floor, and cups stood guard in wobbly towers till neighbors came with coin box yawning empty.",
        "Selling started slow till I shouted 'Free cookie with cup!' Suddenly thirsty friends appeared, and by 2 PM coins overflowed.",
        "Lemon-scented fingers proved little stands build big confidence, especially after counting money later with Mom's praise.",
        "Line shivered with ice cubes melting fast, and our stand became street headquarters where bikes parked making coin collecting math fun.",
        "When rain surprised, we covered the stand with jackets giggling, and damp coins bought pizza dinner for a perfect adventure tale.",
        "Business adventure showed rainy days make best stories, turning ordinary streets into connection places.",
        "Lemon juice stung my papercut, but cups filled steadily as cars slowed making coin pile grow heavy like treasure.",
        "Selling to gardeners and dog walkers built courage, and later buying ice cream felt like pirate spoils from a summer chapter."
    ],
    
    'backyard campout': [
        "Tent poles clicked together after sunset, and fire crackled lighting smores-ready faces as stars blinked awake.",
        "At the top we rested near an old oak tree, and 'Look at these bird nests!' Mom called from behind us during our ride adventure.",
        "Fire sparks chased darkness like firefly dancers, and stars guided finger constellations till eyelids fought in nylon walls.",
        "Sleep arrived late watching moon shadows play tag, and unexpected bird songs woke us at dawn with marshmallow secrets.",
        "Tent assembly caused big arguments, but Mom settled us and fire glowed orange warming October air for cozy stories.",
        "Stars multiplied until sky felt crowded, and snug tent became courage classroom against imaginary fears under moonlight.",
        "Wind tested our tent fiercely, but we held poles strong with fire hugging us in cozy warmth making flapping walls ocean waves.",
        "Cricket lullabies mixed with Dad's snores magically, rocking dream ships home for campers.",
        "Fire cooked canned chili bubbling, and stars witnessed brave bear stories during dewy grass mornings.",
        "Unzipping at dawn, we whispered 'Camping beats pajamas any day!' proving backyards hold universe-sized wonders."
    ],
    
    'bike repair challenge': [
        "Grease decorated fingers like war paint, and wheel refused turning right as ride plans vanished painfully requiring patience lessons.",
        "Finally chain jumped on like a sleepy pet, and spinning wheels brought freedom wings back teaching mechanics need calm minds.",
        "Bike handles shivered dangerously, and grease jar fought opening fiercely during neighbor Pete's coaching on greasy mysteries.",
        "Riding smooth circles later felt miraculous victory, and pedaling sunset streets proved persistence pays in wind rewards.",
        "Training wheel abandon happened with grease spots colonizing jeans, and wheel nuts played hide-n-seek stubbornly needing family brainpower.",
        "Ride finally happened down driveway slopes at dusk, and scraped knees mattered less than conquering wobbles for bike freedom.",
        "Basket sagged like tired arms, and grease smears told fix stories after borrowed pliers and Dad jokes during repair.",
        "Short ride proved recovery complete, and later cruising storeward felt sweeter than pre-fall trips.",
        "Bell silence needed fixing with grease making driveway artwork, and wheel slipped betraying wet paths requiring chain adjustments.",
        "Ride around block proved solutions work when hearts persist, and biking twilight roads sang 'Freedom never quits!'"
    ],
    
    'neighborhood clean-up': [
        "We attacked thorny bushes near Main Street, and street trash surrendered to black bags quickly with candy wrappers, plastic bottles, even an old shoe.",
        "Community warriors worked cheerfully, and Mrs. Wilson told stories about clean streets in her childhood making trash sorting treasure hunt.",
        "Pick sticks clicked rhythmically combing through overgrown lots, and I bagged twenty water bottles calling 'Plastic army alert!' jokingly.",
        "Trash parade to dumpster involved wheelbarrow races and laughter, and finding vintage baseball card felt like neighborhood archaeology.",
        "Gloves shielded hands from poison ivy near creek bank, and street cleaning uncovered history with 1990s baseball trophy half-buried in dirt.",
        "Community pride bloomed with each bag tied shut, and trash talk transformed into 'treasure rescue' stories at celebration picnic.",
        "Gloves marched from Mrs. Parker's porch, and pick teams claimed street territories finding love letters, baby toys, even wartime ration coupons.",
        "When rain surprised, neighbors brought umbrellas and hot chocolate tightening bonds, and final count was 42 bags.",
        "Gloves tore revealing blisters forming during military precision cleanup, and street sparkled post-war against garbage enemies.",
        "Little Lucy's sign 'THANK U CLEAN HEROES' made blisters worthwhile, and sleeping soundly dreamed of dandelions growing through clean cracks."
    ],
    
    'fishing trip surprise': [
        "My line sailed over water smoothly landing near lily pads, and suddenly tug announced strong pull bending pole steeply in unseen battle.",
        "Net scooped up silvery bass dripping rainbows in morning light, and rod hummed with triumph all the way home playing memory like song.",
        "Line sank deep near mysterious bubble clusters, and fish splashed rainbow scales skyward dancing on tail before net saved dinner prize proudly.",
        "Reeling rewards felt like ancient hunter glory, especially when Grandma fried catfish with secret recipe.",
        "Knots frustrated beginner hopes until Grandpa taught special twist untangling with wise fingers, and fish glistened with jeweled defiance.",
        "Net wait made heartbeats drum louder than bullfrogs, and fish dinner tasted crisp adventure around campfire with growing stories.",
        "Ducks cheered silently as I cast line, and knot learning led to tug exploding surface splashily with feisty bluegill landed.",
        "Pan-frying taught cook's happy duty mixing sizzling sounds with cricket songs tasting like growing up.",
        "Line zipped excited reel music during cast at golden hour, and tiny sunfish rewarded patience before release taught conservation appreciation.",
        "Ripples carried little friend home as fireflies blinked approval, proving releasing small ones better than textbooks."
    ],
    
    'cookie baking time': [
        "Mix swirled into sweet symphonies with flour clouds, sugar sparkles, chocolate chip raindrops tempting tasting fingers constantly.",
        "Sweet smells hugged house rooms like invisible hugs, and bake timer pinged perfect moment revealing golden treasures cooling racks display.",
        "Mix demanded careful measurement science with level cups and precise teaspoons, and batter bowls surrendered last scrapings to eager spatulas.",
        "When Dad 'tested' five cookies secretly, we made him wear 'Cookie Monster' sign proving sticky fingers delicious science.",
        "Batter drips painted apron canvas secretly creating edible art, and decorating became serious business with red icing smiles and sprinkle freckles.",
        "Each cookie told story before being eaten, and packaging for neighbors taught sharing joy sweeter than hoarding.",
        "Mix mistakes inspired happy corrections with extra chocolate covering cracks, and 'They're perfect!' insisted Grandma sampling with milk.",
        "Wrapping in foil for lunches made ordinary Tuesday special, and crunchy edges with chewy centers taught imperfections hold delights.",
        "Mix created forever memories with flour fights and spilled vanilla tears during triumphant batch passing around living room.",
        "We invented 'best cookie' awards like 'Most Classic' oatmeal raisin, and messy kitchen proved love measures in cups and teaspoons."
    ],
    
    'school science fair': [
        "Tubes directed vinegar lava flows down cardboard mountains, and watch timed eruptions perfectly bringing shiny blue ribbons during stunned silence.",
        "Bubbles escaped excited reactions, especially when Principal Davis got 'lava' on tie proving science beats clean clothes.",
        "Tubes connected water systems feeding bean plants in different light, and watch monitored thirsty roots hourly unfurling victory leaves.",
        "Result charts whispered plant secrets to patient observers, and green ribbon felt like photosynthesis success.",
        "Tubes rattled with energy transfer proof making paperclips dance like iron ballet, and watch recorded speed changes precisely earning applause.",
        "Physics teacher whispered 'Future engineer!' making cheeks burn hotter than electromagnet when magnets made toy cars zoom without touch.",
        "Tubes held color-changing liquids waiting weeks for magic, and watch counted formation hours journaling crystal spikes like diamond forests.",
        "When blue crystals won 'Most Beautiful', we gave them to kindergarten teachers for wonder windows showing slow science fastest to amazement.",
        "Tubes organized food coloring drops by science rules, and adding soap exploded colors like fireworks rising tiny planets in cosmic milk.",
        "Fair meant proudest class achievement day, especially toddlers pointing at display shouting 'Magic!' during rainbow milk dances."
    ],

    'hidden treehouse secret': [
        "Paper notes sailed wind messages to neighbors using string phones.",
        "Find adventure unfolded summer slow - decoding map found in a bottle.",
        "Hide compartment squeaked open mysteriously revealing forgotten marbles - glass worlds in palm.",
        "We built a museum display in a cigar box, labeling each treasure like archaeologists.",
        "When Sarah hid so well we panicked, her giggle gave position away.",
        "That afternoon proved height offers perspective - both visual and emotional.",
        "Paper codes changed weekly mysteries - invisible lemon juice writing, number ciphers, backward messages.",
        "Finding winter's hidden acorn collection taught us about squirrel preparedness better than any nature documentary.",
        "Paper journals recorded mighty thoughts - rocket designs, peace treaties with ants, poems about dandelions.",
        "That rough wood desk witnessed more creativity than any classroom."
    ],
    
    'grandpas workshop': [
        "Wood smells wrapped memories warm like sawdust hugs.",
        "Build projects included dollhouse magic with real curtains.",
        "Wood shavings perfumed air sweetly, carpeting concrete floor.",
        "When my 'invention' collapsed, Grandpa salvaged parts whispering 'Failures are practice wins.'",
        "Wood grain painted hidden artworks - tiger stripes in oak, storm clouds in walnut.",
        "Build freedom created dream shapes: from crooked toy boats to almost-straight bookends.",
        "Wood waited patient transformation - rough planks becoming picture frames.",
        "Building together, his knobby fingers guiding mine, time folded like fresh-cut paper.",
        "'This saw cut your daddy's cradle,' he said, placing it in my hands.",
        "That afternoon, sawdust became family glitter."
    ],
    
    'beach sandcastle day': [
        "Castle turrets touched heaven until jealous waves threatened invasions.",
        "Water gifted jewel decorations - pearly shells, sea glass gems, crab shell shields.",
        "Waves tickled foundations teasingly before swallowing gatehouses.",
        "Photographers asked to snap our 'sand city' before sunset surrender.",
        "Wave rhythms timed tidal orchestras - advance and retreat.",
        "Sculpting mermaid thrones from wet packs, Sarah crowned herself queen.",
        "Sand wonders dotted shoreline glory - dragon sculptures, turtle mounds, even a sand sphinx.",
        "Sunset painted our city gold before waves reclaimed the canvas.",
        "Castle designs defeated time temporarily - detailed enough for tiny shell doors, sturdy enough for toddler sieges.",
        "When professional sand artists praised our moat system, pride swelled bigger than high tide."
    ],
    
    'puppy rescue mission': [
        "Tiny dachshund shivered beneath leaves, matted fur plastered to bony frame.",
        "Finding reunion ignited backyard dance party when wet nose poked out.",
        "Tracking team followed fresh paw prints to crumbling steps where trembling fur ball hid.",
        "'We'll name him Lucky!' they declared, vet-bound with blankets and hope.",
        "Finding the lost collie sparked block-wide jubilation!",
        "His wagging tail stitched community tighter than decades of polite hellos.",
        "Tracking muddy paw prints taught empathy deeper than schoolbooks.",
        "Watching skeletal pup blossom to glossy show-dog proved love sculpts living masterpieces.",
        "Puppy rescue mission protocol activated: flashlight brigade swept soggy lawns, tracking mud trails to drainage pipes.",
        "Finding shivering pair reunited siblings - tag read 'Milo & Daisy'."
    ],
    
    'school play rehearsal': [
        "Costume chaos reigned - princess tiaras tilted, knight helmets blinded actors.",
        "Final run-through: when my cardboard crown defied gravity, I felt real royalty.",
        "Script memory blanks sparked panic: 'Line? LINE?' echoed backstage shadows.",
        "Practice forged perfection through blunders: thirty run-throughs refined wooden gestures to fluid art.",
        "Backstage chaos schooled teamwork: zipping gowns while whispering cues, safety-pinning costumes mid-monologue.",
        "When Velcro failed during death scene, quick-thinking stagehand used duct tape rescue.",
        "Line delivery practice birthed characters: villains found sneery voices, heroes discovered thunder tones.",
        "Thursday's breakthrough: during storm scene, real rain leaked through roof! Improvised umbrella dance got biggest applause.",
        "Costume crowns finally cooperated with industrial tape.",
        "After-party glittered with wrinkled costumes sharing tales: ripped corset from passionate embrace, helmet worn backward in Act II."
    ],
    
    'family hiking trip': [
        "Walk pace adapted to littlest legs: 'Stop! Caterpillar crossing!' demanded Emily.",
        "Summit rest revealed wind-whispered secrets as hawks circled below.",
        "Rest benches framed valley masterpieces - toy-sized villages, rivers ribboning through forests.",
        "Snack-sharing became diplomacy: trail mix trades for granola bars.",
        "Silent intervals soaked nature symphonies: woodpecker drums, squirrel scolds, whispering pines.",
        "Thunder surprised at mile three - shared poncho became giggling tent fortress.",
        "Victory snacks tasted ambrosial - crisp apples echoing crunch, gorp like gold coin treasure.",
        "Group photo showed wind-whipped hair and conquering grins.",
        "Wrong turn magic: hidden waterfall discovery!",
        "Twilight return carried more than tired legs: squirrel encounters, geology lessons, cloud shape debates."
    ],
    
    'stormy night experience': [
        "Lightning flashes painted ghostly wall murals - dancing giants throwing thunderbolts.",
        "When hail drummed rooftop, kitchen fort construction began with blanket artillery.",
        "Candle flames birthed shadow puppet theater - rabbit ears twitching, eagle wings soaring, dinosaur jaws snapping.",
        "When lights flickered on, groans proved we preferred magical darkness.",
        "Flashlight beams became valiant knights slaying shadow dragons.",
        "Midnight snack raid uncovered cookie treasures - sweet comfort against nature's fury.",
        "Lightning strikes counted fearfully - eight in twelve minutes!",
        "Harry Potter reading by flicker-light made magic realer than thunder.",
        "Family story marathon began: Mom's childhood blizzard survival, Dad's tornado drill memory.",
        "Pillow fort engineering reached cathedral proportions - sofa foundation, blanket domes."
    ],
    
    'bike parade fun': [
        "Bike carnival rolled joyfully - unicorns prancing, fire trucks wailing, clowns zigzagging.",
        "Crowd cheers rocket-fueled tired legs uphill.",
        "Ride procession ordered ranks: veterans leading, wobbly kids mid-pack, grandparents guarding rear.",
        "When professional sand artists praised our moat system, pride swelled bigger than high tide.",
        "Glitter-bombed bikes rolled over pavement red carpet.",
        "When Mr. Dale's 1950s bicycle won 'Most Classic', chrome outshone his proud tears.",
        "Drum corps beats jumpstarted pedal energy.",
        "Cheer wave swept sidewalks with rhythmic clapping.",
        "Chalk artists transformed asphalt into rainbow road.",
        "Post-parade chalk cleanup painted gutters temporary rainbows - liquid memories draining toward next year."
    ],
    
    'secret recipe discovery': [
        "Ingredients whispered family secrets: stained margarine notes, spice measurements smelling of history.",
        "Oven magic summoned ghostly vanilla perfume.",
        "Heirloom ingredients held fingerprints: cracked cinnamon jar from Italy, vanilla bottle from Aunt May's honeymoon.",
        "Taste explosion awakened dormant memory: 'Nana's cookies!' Mom cried, reviving flavors lost fifty years.",
        "Mixing channeled ghostly guidance - 'More nutmeg!' imagination insisted.",
        "Golden moon cookies finally emerged.",
        "Texture achieved magic balance: crisp lace collars hugging chewy middles.",
        "Neighbor tins included recipe photocopies - delicious virus spreading.",
        "Passing stained recipe clockwise, we added names below Grandma's cursive.",
        "'Generation Four Bakers' headed parchment now tucked in cookbook shrine."
    ],
    
    'vegetable garden help': [
        "Shovel conquered concrete-like soil, revealing fragrant chocolate earth.",
        "Water ceremony blessed seedlings from rainbow sprinkler.",
        "Bean tepee engineering required deep shovel bites.",
        "Growth measurement became morning ritual: 'Beanstalk climbed three inches!'",
        "Scientific observation proved beans grow faster sung to - off-key tunes embarrassed birds.",
        "Harvest festival celebrated bounty: cucumbers measured for ribbons, peppers rated for firepower.",
        "Dinner table transformed classroom: 'My peas!' kids bragged serving homegrown stars.",
        "After preserving jars gleamed pantry rainbows, dirty fingernails testified: connection grows deepest roots."
    ],
    
    'lost toy search': [
        "Search mission deployed: flashlight swept bushes, siblings interrogated.",
        "Finding miracle occurred atop laundry mountain - peeking from jeans pocket!",
        "Excavation recovered mud-fossil treasures washed to glory.",
        "Princess Glitter's rescue interrupted Mr. Wilson's chore.",
        "Sofa cushion excavation revealed robot hostage.",
        "Search perseverance taught resilience: tears dried by discovery grins."
    ]
}

NARRATIVE_EXAMPLES4K = {
    'baking disaster': [
        "Our chocolate chip cookies looked like charcoal briquettes.",
        "But Mom saved the day: 'Let's make cookie ice cream sandwiches!' Crumbling the disaster cookies over vanilla ice cream created a new sweet treat.",
        "Flour poofed like a cloud when the mixer went too fast, dusting the kitchen white.",
        "But Grandma taught us redemption: blending the burnt bits into milkshakes.",
        "Charred cookie corpses filled the pan, hard as hockey pucks.",
        "Just as tears threatened, Mom arrived with genius: 'Let's make trifle!' Layering crumbled cookies with pudding and fruit created edible art.",
        "The oven timer screamed too late - our cookies were tan soldiers marching in formation.",
        "But creativity saved the day: crushing cookies over yogurt created instant parfaits.",
        "Our mess became modern art - beige blobs sliding down stainless steel.",
        "Dipping the survivors in melted chocolate hid their imperfections. Those lopsided treats tasted like victory over kitchen chaos."
    ],
    
    'garden harvest': [
        "Tomato vines sagged with ruby treasures begging to be picked.",
        "Dirt smudged our knees as we crawled through green tunnels. Each pick felt like finding nature's candy - warm, sweet, and perfect.",
        "Vines whispered secrets as we filled baskets until sunset painted the garden gold.",
        "Seed miracles amazed us: tiny dots transformed into heavy fruits.",
        "Vine jungles hid the biggest tomatoes, shy giants blushing crimson.",
        "Canning jars lined up like soldiers waiting for transformation. Preserving summer's warmth became our rainy day project.",
        "Dirt paths became treasure trails leading to hidden clusters.",
        "Seed starting memories flooded back - tiny sprouts under grow lights last March.",
        "Pick movements slowed to savor each pluck as tomato plants offered final gifts before frost.",
        "Preserving the harvest became loving ritual, sealing summer in jars like captured sunlight."
    ],
    
    'bike repair challenge': [
        "Grease covered my fingers as I wrestled the stubborn chain.",
        "Testing it around the block, wind kissed my face again. Freedom tasted like grease and victory.",
        "Grease jar opened reluctantly, smelling like mechanical hope.",
        "Ride around the driveway proved success - wobbly but working.",
        "Bike brakes squealed like angry cats.",
        "Ride test down the hill brought smooth silence - music to my ears! Stopping perfectly at the bottom felt like conquering mountains.",
        "Bike gears jammed with mysterious gunk.",
        "Ride through the park afterward felt like flying with new wings.",
        "Bike pedal snapped off mid-stride! Grease-covered investigation showed stripped threads.",
        "Ride home after repair felt extra careful - testing each rotation like walking on ice."
    ],
    
    'rainy day fort': [
        "Build plans evolved - first a simple tent, then a castle with towers!",
        "Storm winds howled outside while we read comics by flashlight. Blanket walls blocked grown-up world perfectly.",
        "Build engineering required chair architecture and clothespin clips.",
        "Storm rumbles made our blanket roof shiver excitingly.",
        "Indoor world transformed - sofa became mountain, carpet turned lava sea.",
        "Storm flashes lit our hideout like disco parties.",
        "Build masterpiece featured three rooms and a secret exit.",
        "Blanket ceiling sagged heroically under stuffed elephant weight.",
        "Build version 3.0 included drawbridge and moat (socks).",
        "Blanket walls absorbed our laughter like acoustic clouds."
    ],
    
    'lost library book': [
        "'Where is it?' I panicked, tearing my room apart.",
        "Page-flipping ghost seemed to hide it! Finally, beneath the hamster cage - success!",
        "Book disappearance sparked household detective work.",
        "Page 42 peeked from under the car seat!",
        "Library book vacation extended mysteriously.",
        "Page corners finally appeared beneath the sofa cushion!",
        "Book hiding skills amazed me.",
        "Find celebration erupted when it surfaced in the picnic basket - damp but readable!",
        "Shelf ghosts seemed to swallow 'Pirate Tales'.",
        "Find miracle happened in Dad's briefcase - 'Must've borrowed it!' he laughed."
    ],
    
    'family pizza night': [
        "Dough flew like frisbees during Friday pizza night.",
        "Slice cutting released steamy aromas making tummies roar.",
        "Cheese shredding turned into snowfall over sauce seas.",
        "Slice sharing became taste-test diplomacy. Crunchy crust sounds harmonized with contented munching.",
        "Oven warmth hugged the kitchen like a blanket.",
        "When cheese strings connected mouth to slice, laughter stretched longer.",
        "Oven light watched our creations bubble and brown.",
        "Slice perfection was judged by crispiness and cheese pull length.",
        "Oven became time machine smelling like childhood.",
        "Slice cutting ceremony commenced when Grandpa declared 'Ready!' Cheese strings connected us like edible threads."
    ],
    
    'school art project': [
        "Messy hands became rainbows - blue knuckles, yellow palms, green fingernails.",
        "Our gallery walk later showed that messy art dries beautiful.",
        "Brushes became magic wands transforming white to wonder.",
        "Color explosions decorated not just paper but shirts, faces, and floor tiles.",
        "Brush techniques varied - dabbing dots, swirling storms, stabbing stars.",
        "Color theory in action: blue + yellow = green magic.",
        "Brush strokes whispered secrets - light touches for clouds, heavy drags for mountains.",
        "Color mixing became science and sorcery - creating 'dragon blood red' from pink and brown.",
        "Brushes of all sizes enlisted for textural warfare.",
        "Draw together project connected our papers into one long mural telling a class story."
    ],
    
    'camping tent trouble': [
        "Rain started just as we finished, testing our waterproof claims. Stake hammering became mud-splattering comedy.",
        "That stormy night taught us tents are cozy caves against nature's fury.",
        "Stake refusal in rocky soil required creative rock weighting.",
        "Sleep finally came wrapped in damp sleeping bags.",
        "Wind turned our shelter into a nylon balloon.",
        "That leaky tent bonded us more than perfect weather ever could.",
        "Stake hammering echoed through the campground attracting amused neighbors.",
        "Wind added drama by trying to carry away our half-built shelter.",
        "Stake loops tore under pressure when wind conducted the nylon flapping symphony all night.",
        "That troubled tent became legend - 'Remember the trip when...' stories for years."
    ],

    'lemonade stand success': [
        "'Squeeze harder!' my sister said, pressing lemons into the pitcher. Cups lined the wobbly table neatly.",
        "First customer was Mr. Brown walking his dog. 'Two cups please!' he said, dropping coins that jingled happily.",
        "'Ice cold lemonade!' my brother yelled. Mrs. Parker bought four cups for her gardening club.",
        "Heat wave perfect for lemonade business! Lemons rolled off the counter as we squeezed. Cups stacked in colorful towers.",
        "Coin jar overflowed! Final count: $21.40. We bought pizza for dinner with our earnings.",
        "Lemon juice stung my paper cut but I kept squeezing. Cups wore handmade 'Best in Town' stickers.",
        "Coin rain filled our jar steadily. When temperature hit 90°, sales doubled.",
        "'Thirsty? Stop here!' signs worked. Customers included joggers, bikers, dog walkers.",
        "Piggy bank gained weight, our arms gained freckles. Simple stand taught big money lessons."
    ],
    
    'broken window mystery': [
        "Glass shards glittered on the grass. Find mission began - what caused this? Ball sat suspiciously near the fence.",
        "'Did you kick it here?' I asked my brother. He shook his head nervously. Who did this? Mystery deepened.",
        "Glass fragments twinkled in flower bed. Find the culprit became urgent. Ball rested guiltily near roses.",
        "Footprints in soft soil led to the fence. Blue thread snagged on rose bush matched Tommy's shirt.",
        "Glass confetti covered the patio. Find what caused it - now! Ball sat innocently under chair.",
        "Magnifying glass revealed tiny feathers near the break. Bird strike! A robin flew into the window.",
        "Window looked like a frozen pond with cracks. Glass pieces winked in sunlight.",
        "Flashlight found scuff marks below the window. Paw prints in dirt! Neighborhood dog chased a squirrel up the wall.",
        "He admitted testing his ball skills alone. Grounded for a week, he saved allowance for repair."
    ],
    
    'hidden treehouse note': [
        "Tree branches swayed in the storm while I found loose floorboard treasure. Paper slightly damp but perfect for messages.",
        "'Finder: seek blue rock by creek' I printed clearly. Hide spot chosen carefully under the red cushion.",
        "Next morning, Sammy's excited shout echoed: 'I found it! Real marble treasure!' His joyful dance made rainy day magic.",
        "Write faded but clear: 'Full moon meeting place'. Hide cleverly where only curious eyes would see.",
        "Windy afternoon blew unexpected paper into our sanctuary. Tree branches cradled it like a precious gift.",
        "Small words sparked big talk about school challenges. Paper connection bridged our friendship deeper than before.",
        "Write operation details: 'Cookie raid - kitchen, 3 PM sharp!' Hide inside the special knot-hole we call 'mailbox'.",
        "Mission succeeded - warm chocolate chips tasted doubly delicious after covert planning.",
        "Next morning, our lawn held paper plane with smiley face reply. Neighborhood game began - message magic connecting yards and hearts."
    ],
    
    'grandpas workshop': [
        "Saw buzzed through pine like warm knife through butter. Build project: bluebird house! Nail hammering made rhythmic music - tap-tap-BANG!",
        "'Measure twice!' Grandpa reminded, tape snapping wisdom. Dust coated my arms like powdered sugar.",
        "Tool bench wore wood shavings like confetti. Wood scraps became sailing ship with toothpick masts.",
        "Saw carefully followed pencil lines, curls falling like golden ribbons. Build slowly - no rushing art.",
        "Tool box creaked open releasing oil and memory smells. Wood pieces became picture frames for family photos.",
        "Saw sang its high-pitched song, dust motes dancing in window light. Build something useful together.",
        "Saw dust flew in golden clouds, tickling noses. Build carefully, sanding edges smooth.",
        "When Mom opened it, her tears matched the polished wood shine. Hands build more than objects.",
        "Broken stool repair mission. Tool drawer announced opening with metallic song. Wood glue applied with popsicle stick precision."
    ],
    
    'beach sandcastle contest': [
        "Sand squished between happy toes as buckets filled. Castle rose with triple towers connected by bridges.",
        "Wave sneak-attacks tested moat defenses. Dig trenches deeper, walls thicker. Tower flags fluttered - seashells on twigs.",
        "Castle evolved into fortress with drawbridge and secret tunnels. Wave assaults came regularly - moats held strong!",
        "Dig teams formed: moat-diggers, wall-builders, decorators. Tower taller than Dad!",
        "Sand cooled sunburned feet during construction. Castle complex featured main keep, outer walls, and guard towers.",
        "Wave washed south wall away - 'Rebuild stronger!' Dad encouraged. Dig faster, teamwork tighter.",
        "Sun-drenched contest morning. Sand sculpted like cold clay under fingers. Castle decorated with treasure: striped seashells, blue glass gems.",
        "Tower building tips from experienced Grandpa proved invaluable. Prize certificate for 'Best Teamwork' now on my wall.",
        "Afternoon sun slanted long shadows. Sand stuck to sunscreen like glitter glue. Castle village for plastic knights - cottages, market square, cathedral."
    ],
    
    'sunday morning pancakes': [
        "Pan sizzled as butter danced. Batter poured in perfect circles that bubbled like mini volcanoes.",
        "Flip practice made perfection after one soggy casualty. Syrup river flowed golden over stack mountain.",
        "Batter hid blueberry surprises like edible jewels. Flip challenge - how high? First one folded sadly.",
        "Table gathered hungry tribe - cousins, grandparents, dogs begging. Stack grew skyscraper tall.",
        "Flip expertise - spatula slide-toss-catch! Syrup authentic Vermont maple, pricey but sacred.",
        "Batter flecked with chocolate chips like edible constellations. Flip contest - mine reached ceiling!",
        "Rainy Sunday demanded comfort cooking. Pan sang butter songs. Batter puffed into fluffy clouds on hot surface.",
        "Double flip landed perfectly. Syrup waterfall cascaded down stack slopes.",
        "Table full: Dad reading paper, Mom slicing fruit, kids drawing. Stack challenged gravity."
    ],
    
    'soccer game mishap': [
        "Ball rolled onto rain-slick grass. Kick-off sent it flying. Mud splattered uniforms like war paint early on.",
        "Sudden downpour turned field to soup. Final kick slipped wide - missed opportunity.",
        "Kick attempt slipped - faceplant in turf! Mud baptized my new cleats.",
        "Team cheers lifted spirits higher than embarrassment. After practice, muddy mess took garden hose cleanup.",
        "Ball felt heavy as cannonball. Kick connected perfectly - SWOOSH! Mud puddle swallowed the ball unexpectedly.",
        "Ball hit hidden rock - POW! Kick sent it sailing over fence into Mr. Henry's garden.",
        "Grass stains became badges of effort. Sometimes broken rules lead to new friends.",
        "Kick practice finally paid off - perfect corner shot! Mud battle royal when rain began.",
        "Team dogpile hug celebrated in pouring rain and mud. Sportsmanship shines brightest in messy moments."
    ],
    
    'school science experiment': [
        "Mix baking soda volcano waited - white powder mountain. Vinegar poured - bubble eruption overflowed!",
        "Tube directed lava flow across 'village' diorama. Watch foam grow like living creature.",
        "Mix food colors in test tubes - red, yellow, blue. Bubble reactions swirled like miniature galaxies.",
        "Watch transformations as solutions mingled. React with hypothesis notebooks.",
        "Mix oil and water in clear jugs. Bubble patterns formed geometric art as we shook.",
        "Watch in awe at stubborn refusal to blend. React with insightful questions about density.",
        "Mix cornstarch and water discovery. Bubble? No - instant oobleck!",
        "Tube tested flow rate - solid under pressure, liquid when relaxed. Watch as it defied categories.",
        "Mix hot and cold water in soda bottle. Bubble clouds formed when pressure changed.",
        "Watch miniature storm develop behind glass. React with amazed applause for atmospheric magic."
    ],

    'lost puppy search': [
        "Tracks in the mud led toward busy Main Street. My heart pounded tracking paw prints through neighbor's gardens.",
        "Find mission felt hopeless until a tiny whimper under Mrs. Gable's porch.",
        "'Milo! Cookie!' we called desperately. Tracks appeared near creek bed - tiny paws in mud.",
        "Under willow tree, soaked ball of fur whimpered. 'Safe now!' we cuddled him.",
        "'Scout come!' children called. Tracks crossed four streets surprisingly.",
        "Behind elementary school, shaking pup hid in bushes. 'Home safe!' celebration began.",
        "'Baby! Treats!' we called shaking kibble bag. Tracks followed scent trail to park.",
        "Find moment: sleeping puppy near duck pond. 'Got you!' whispered hug.",
        "Happy reunion proved even small creatures leave big holes in hearts when gone."
    ],
    
    'fishing trip surprise': [
        "Unexpected tug nearly pulled pole away! Fish fought like monster beneath lily pads.",
        "Net barely contained wriggling bass. 'Biggest catch ever!' Dad yelled proudly.",
        "Gentle tug became fierce battle. Fish jumped shining rainbow scales!",
        "Net grabbed it mid-air splashily. 'Beautiful trout!' Grandpa admired.",
        "Unexpected tug shocked sleepy mind! Fish fought fiercely for freedom.",
        "Small tug became serious wrestling match. Fish leaped dancing on water!",
        "Massive tug bent pole steeply. Fish fought thirty heroic minutes.",
        "Net strained under its weight. 'Giant catfish!' we marveled.",
        "Pond surrendered legendary creature surprising everyone."
    ],
    
    'cookie jar mystery': [
        "Empty! Only crumbs remained inside. Clue hunt began: chocolate smudge on counter.",
        "Find led to little brother hiding with bellyache. 'Too tasty!' he confessed.",
        "Jar lid sat crookedly. Empty evidence suggested thief. Clue: flour footprints to playroom.",
        "Find culprit building cookie fort with last chocolate chip.",
        "Empty sound echoed disappointing. Clue: white powder on sofa.",
        "Find mission tracked to giggling dog with crumb beard.",
        "Empty! Disaster declared. Clue: ladder near counter.",
        "Find: Dad napping with cookie coma. 'Just one... became five!' he confessed.",
        "Sweet mystery united bickering siblings."
    ],
    
    'bicycle parade fun': [
        "Streamers like rainbow rivers flowing behind wheels. Ride procession rolled past cheering crowds.",
        "'Go riders!' shout vibrated air. Cheerful chaos painted happiness on faces.",
        "Flags whipped wind excitement. Streamers tangled until teamwork triumphed.",
        "Crowds multiplied at each block. 'Beautiful bikes!' cheers multiplied smiles.",
        "Flag poles attached creatively. Streamers wound spokes colorfully.",
        "Crowd families lined sidewalks early. 'Fantastic!' comments fueled pedals.",
        "Streamers competed length and colors. Ride route circled lake shore.",
        "Crowd cheered loudest for kids' wobbles. 'You're stars!' encouragement strengthened small legs.",
        "Wheels spun funds for good causes."
    ],
    
    'secret family recipe': [
        "Ingredients listed in Grandma's looping handwriting: 'nutmeg, love, patience'.",
        "Mix instructions specified clockwise stirring while humming childhood songs.",
        "Paper found tucked in her worn cookbook, edges softened by time.",
        "Smell revived her appetite - first real meal in weeks! Taste of warm apple pie transported her to healthier days.",
        "Paper emerged from the antique recipe box, ink faded but legible.",
        "Mix technique demonstrated by Aunt May - folding not beating.",
        "Paper recipe brittle as autumn leaves, dated 1923.",
        "Smell permeated school hall - teachers followed the aroma.",
        "Smell declared this house home - cinnamon and love permeating walls."
    ],
    
    'stormy power outage': [
        "Candles flickered timidly, painting dancing giants on walls.",
        "Storm raged outside - hail drumming roof like angry fists.",
        "Candles dripped wax rivers across the tablecloth. Flashlight tag entertained kids - light spots chasing giggles.",
        "Family built blanket palace under dining table. Game tournament commenced: charades championship by candlelight.",
        "Dark revealed unfamiliar shapes: coat racks became lurking monsters.",
        "Family invented indoor campout: sleeping bags by fireplace.",
        "Candles scented the air with calming lavender.",
        "Family became story circle: each sharing childhood memories.",
        "Power returned unnoticed during laughter-filled storytelling."
    ],
    
    'backyard campout': [
        "Fire finally crackled after three matches and much blowing.",
        "Marshmallows sparked joyful debates: 'Golden brown is art!' vs 'Charred is character!'",
        "Tent assembly required parental rescue - poles snapping stubbornly.",
        "Stories grew scarier with each rustle - 'Was that a bear?'",
        "Fire pit glowed center stage, embers winking like fireflies.",
        "Stories created elaborate shared worlds - superhero squirrels saving acorns.",
        "Fire rescued damp spirits - steaming socks by flames.",
        "Shared experience deepened understanding beyond words, fire reflecting in thoughtful eyes.",
        "Sleeping under strange stars felt courageous and comforting simultaneously."
    ],
    
    'community garden help': [
        "Shovels distributed to volunteers - neighbors becoming friends.",
        "Planting became joyful party: 'Pass the petunias!'",
        "Flowers chosen for butterfly appeal - nature's rainbows.",
        "Watering schedule arranged cooperatively - Mrs. Lee's morning shift.",
        "Shovel work opened blisters proudly - badges of effort.",
        "Planting ceremony included Mariachi band - soil dancing.",
        "Flowers chosen for sensory delight: fragrant lavender, velvety pansies.",
        "Planting involved all abilities - shared accomplishment glow.",
        "Community grew stronger than weeds, united by fertile ground."
    ],
    
    'school play rehearsal': [
        "Script pages crinkled nervously in trembling hands.",
        "Stage felt terrifyingly large under hot lights.",
        "Costumes transformed ordinary kids into kings and peasants.",
        "Practice smoothed rough edges nightly - repetition mother of skill.",
        "Costumes designed creatively cheap - cardboard crowns glittered.",
        "Script revisions last-minute - 'Santa needs more lines!'",
        "Costumes mixed modern jeans with period doublets.",
        "Stage fright almost won - nausea before entrance.",
        "Costumes created from recycled materials - plastic bottle armor."
    ]
}

NARRATIVE_EXAMPLES5K = {
    'community garden project': [
        "Garden beds needed fresh soil - shovels dug deep turning earth.",
        "Seed miracles amazed us - tiny dots becoming food.",
        "Garden paths needed weeding - shovels scraped stubborn roots.",
        "Little Mia discovered a ladybug on pepper leaves. 'Protector bug!' she whispered.",
        "Garden soil hardened from winter - shovels broke crusts.",
        "Kids painted garden signs with bright vegetables.",
        "Summer heat challenged gardeners. Shovels turned dry soil carefully.",
        "Sharing stand appeared at garden gate: 'Take what you need.'",
        "Fall cleanup day bittersweet. Shovels prepared beds for winter sleep.",
        "Kids buried time capsule with garden wishes."
    ],
    
    'bicycle repair adventure': [
        "Grease covered my fingers as I wrestled stubborn links.",
        "Testing around the block, wind kissed my face again. Freedom tasted like grease and victory.",
        "Grease jar opened reluctantly. Wheel nuts resisted my small wrench.",
        "Ride around driveway proved success - wobbly but working.",
        "Brakes squealed like angry cats. Grease smeared my jeans during adjustments.",
        "Ride test down hill brought smooth silence - music to ears!",
        "Gears jammed with mysterious gunk. Grease cleaning revealed missing teeth on rear cog.",
        "Ride through park afterward felt like flying with new wings.",
        "Pedal snapped off mid-stride! Grease-covered investigation showed stripped threads.",
        "Ride home after repair felt extra careful - testing each rotation."
    ],
    
    'sunday pancake breakfast': [
        "Batter poured in perfect circles bubbling like mini volcanoes.",
        "Flip practice made perfection after one soggy casualty.",
        "Batter hid blueberry surprises like edible jewels.",
        "Flip challenge - how high? First one folded sadly.",
        "Batter thin for lacy edges crisping perfectly.",
        "Flip expertise - spatula slide-toss-catch!",
        "Batter flecked with chocolate chips like edible constellations.",
        "Flip contest - mine reached ceiling!",
        "Batter puffed into fluffy clouds on hot surface.",
        "Flip show-off time - double flip landed perfectly."
    ],
    
    'lost library book hunt': [
        "'Where is it?' I panicked tearing room apart.",
        "Page-flipping ghost seemed to hide it! Finally beneath hamster cage - success!",
        "Library notice glared from fridge. Shelf investigation yielded dust bunnies but no novel.",
        "Page 42 peeked from under car seat!",
        "Shelf check showed empty space where 'Dinosaur Facts' lived.",
        "Page corners finally appeared beneath sofa cushion!",
        "Shelf ghosts seemed to swallow 'Pirate Tales'.",
        "Find miracle happened in Dad's briefcase - 'Must've borrowed it!' he laughed.",
        "Book hiding skills amazed me.",
        "Find celebration erupted when it surfaced in picnic basket - damp but readable!"
    ],
    
    'family pizza night': [
        "Dough stretched between my hands like magical rubber.",
        "Toppings selection turned into family debate - 'Pineapple belongs!' vs 'Never!'",
        "Dough edges bubbled in hot oven releasing delicious smells.",
        "Cheese melted into golden perfection with pepperoni islands floating.",
        "Dough-tossing skills like pizzeria pro - 'Watch the spin!'",
        "Toppings became geography lesson - 'Here's olive mountains!'",
        "Sister spread sauce making 'volcano craters'.",
        "Cheese-sprinkling job created snowy mountain ranges.",
        "Grandpa taught ancient dough-stretching techniques.",
        "Toppings selection included garden-fresh herbs."
    ],
    
    'rainy day fort building': [
        "Blankets flew from linen closets as we planned.",
        "Building construction caused minor collapses requiring redesign.",
        "Blankets draped over furniture creating magical tunnels.",
        "Building challenges required engineering solutions.",
        "Blanket collection became architectural challenge.",
        "Building design evolved from simple tent to multi-room complex.",
        "Blankets smoothed over bookshelf foundations.",
        "Building process taught cooperation and compromise.",
        "Blanket collection covered entire family room.",
        "Building became collaborative engineering project."
    ],
    
    'school art class': [
        "Paint pots crowded tables with rainbow options.",
        "Color mixing taught magical transformations - red+yellow=orange!",
        "Paint splattered aprons creating wearable art.",
        "Color experiments produced surprising results.",
        "Paint danced making waves and whales.",
        "Color explosion matched joyful mood.",
        "Paint cups arranged like soldiers ready.",
        "Color flowed freely without restraint.",
        "Paint flew creating accidental masterpieces.",
        "Color mixed directly on surfaces experimentally."
    ],
    
    'lemonade stand success': [
        "'Lemonade for sale!' we chanted. First customer was Mr. Wilson walking his dog - 'Two cups please!'",
        "Coin jar started filling slowly. Neighbor kids came next, buying refills.",
        "Lemons escaped my slippery grip, rolling downhill. 'Catch them!' yelled sister chasing like cartoon characters.",
        "Coin counting concluded with surprising $21.75!",
        "'Thirst solution here - 50 cents!' our sign announced.",
        "Coin jar gained weight satisfyingly.",
        "Lemon juice stung my paper cut painfully.",
        "Coin collection jingled like tiny bells calling customers.",
        "Juicy lemons surrendered nectar after energetic squeezing.",
        "Profit $19.50 bought ingredients for next weekend's business."
    ],
    
    'backyard camping': [
        "Tent poles clicked together satisfyingly under setting sun.",
        "Stars emerged like diamond dust on velvet sky.",
        "Tent assembly took teamwork - poles fighting, fabric tangling.",
        "Sparks danced like crazed fireflies mesmerizing us.",
        "Tent construction required Grandpa's expertise and our eager hands.",
        "Star-gazing sparked questions about universe and our place in it.",
        "Tent stood strong against surprise midnight rain shower.",
        "Fire rescued damp spirits with warming flames and drying assistance.",
        "Tent smelled like new adventure possibilities.",
        "Fire cooked surprisingly delicious foil-packet potatoes and sausages."
    ],
    
    'broken window mystery': [
        "Front window displayed growing crack like shattered ice.",
        "Investigation began: backyard search revealed baseball near rhododendrons.",
        "Kitchen window showed spiderweb fracture pattern.",
        "Clever clue hunting: grass stain on ball matched Jake's glove.",
        "Stormy night hid window damage until morning.",
        "Flashlight investigation revealed muddy paw prints on wall beneath window.",
        "Sunrise revealed shattered dining room window scene.",
        "Mud trail led to fence opening. Paint scrape on window sill matched skateboard ramp color next door.",
        "Severe storm caused midnight window casualty.",
        "Careful inspection found rotting window frame - structural weakness."
    ],
    
    'neighborhood clean-up': [
        "Gloves distributed at park gazebo - various sizes for all hands.",
        "Street trash collection became treasure hunt: bottle caps, lost toys, even vintage soda can.",
        "Bright yellow gloves made teams visible blocks away.",
        "Kids competed finding 'weirdest trash' - winner discovered antique perfume bottle.",
        "Protective gloves shielded against broken glass dangers.",
        "Street cleaning uncovered neighborhood history - 1950s toy car, vintage soda bottle.",
        "Glove handouts launched neighborhood movement.",
        "Street discoveries created historical curiosity: old newspapers, porcelain fragments.",
        "Durable gloves needed replacing after snagging sharp objects.",
        "Street beauty emerged visibly: blooming flowers previously hidden by litter."
    ],

    'fishing trip surprise': [
        "Unexpected powerful tug tested pole strength almost pulling it away!",
        "Fish battled below creating swirling vortex.",
        "Strong sudden tug startled peaceful meditation.",
        "Fish leaped spectacularly silver body flashing in sunlight fighting freedom.",
        "Determined hard tug signaled something substantial.",
        "Fish scales flashed rainbow colors as it fought fiercely.",
        "Sudden intense tug interrupted quiet contemplation.",
        "Fish surrendered after worthy ten-minute duel - worthy opponent.",
        "Unanticipated violent tug surprised complacent afternoon.",
        "Fish taught valuable patience and presence lesson."
    ],
    
    'cookie baking time': [
        "Mix ingredients combined rhythmically: sugar clouds, flour snowfall, egg volcanoes.",
        "Sweet vanilla aroma perfumed entire house permeating curtains.",
        "Mix precision required focus: level measurements, gradual additions.",
        "Sweet samples vanished mysteriously from cooling racks - blamed on cookie monsters.",
        "Mix spatula danced creatively smoothing cookie mountains.",
        "Sweet anticipation filled kitchen like rising dough.",
        "Mix masterpiece awaited baking - carefully scooped dough mounds.",
        "Sweet moments measured in cooling rack rotations.",
        "Mix science created edible art: chocolate chunk islands, oatmeal raisin landscapes.",
        "Sweet history lesson as Grandma shared recipe origins."
    ],
    
    'bicycle parade fun': [
        "Bike streamers fluttered colorful announcements signaling parade start.",
        "Ride formations practiced for weeks: V-patterns, parallel lines.",
        "Ride groups formed smiling squadrons: superheroes, pirates, animals.",
        "Crowd encouragement flowed generously along route: 'You're stars! Looking great!'",
        "Pavement welcomed rolling artworks: card table bike spaceship, tricycle dragon.",
        "Special recognition category winners caused happy tears during announcements.",
        "Ride transformed ordinary pavement into rainbow river temporarily.",
        "Turning onto Main Street seeing familiar faces beaming validated weeks of preparation.",
        "Colorful runoff during post-parade cleaning became liquid celebration memories.",
        "Simple parade created lasting unity memories."
    ],
    
    'secret recipe discovery': [
        "Ingredients whispered generational secrets: nutmeg magic, spice mysteries.",
        "Mix process involved ancestral techniques: wooden spoon clockwise stirring.",
        "Ancestral ingredients measured traditionally - teacups, pinches, dashes.",
        "Mix ritual followed faded instructions: fold gently, beat enthusiastically.",
        "Mix trials created kitchen laboratory experimentation.",
        "Taste inconsistencies drove research obsession: oven calibration? Ingredient freshness?",
        "Mix techniques perfected through delicious repetition.",
        "Taste consistency achieved after recipe translation: 'Grandma's pinch' measured scientifically.",
        "Original recipe card placed in archival frame with new signatures below.",
        "Taste-tested memorial batch connected past-present-future deliciously."
    ],
    
    'stormy power outage': [
        "Thunder rattled window frames violently shaking pictures.",
        "Candlelight conquered shadow fears creating cozy islands.",
        "Howling wind threatened security rattling doors.",
        "Flashlight beam puppetry created courageous heroes saving the day.",
        "Lightning flashes illuminated rooms briefly like camera flashes.",
        "Reading together restored normalcy magically - adventure novels by flickering light.",
        "Game competitions diverted anxiety: charades, board games by candlelight.",
        "Blanket fort construction involved complex engineering.",
        "Candlelight procession through dark house became ceremonial.",
        "Flashlight tunnels amused toddlers crawling through beams."
    ],
    
    'hidden treehouse note': [
        "Paper treasure discovered under loose floorboard!",
        "Message writing sparked adventure planning: 'Treasure buried near blue rock'.",
        "Tree trunk concealed clever compartment near window ledge.",
        "Ancient faded writing puzzled investigators: 'Midnight meeting required'.",
        "Wind-assisted delivery amazed us with folded perfection.",
        "Message addition felt appropriate: 'You brave! - from sky friend'.",
        "Paper notes passed silently: 'Operation Dessert: 3 PM sharp!'",
        "Protective hiding in knot-hole mailbox implemented carefully.",
        "Drifting paper airplane landed miraculously on platform.",
        "Message reply written quickly: 'Hello sky-friend! Join me!'"
    ],
    
    'grandpas workshop day': [
        "Tool wall stood orderly: hammers saluting, screwdrivers waiting.",
        "Saw buzzed through pine singing creation song.",
        "Wood transformation fascinated me - raw plank to toy sailboat.",
        "Saw discipline required focus: follow pencil lines exactly.",
        "Tool accessibility invited participation: 'Choose your weapon!'",
        "Angled cuts demonstrated practical geometry applications.",
        "Sawdust flew like golden snow during careful cutting.",
        "Hinging required magnifying glass precision and deep breathing.",
        "Tool selection methodical: clamps before glue.",
        "Wood repair honored decades of service - filling cracks carefully."
    ],
    
    'sandcastle competition': [
        "Wave threats considered strategically: deep trenches, high walls.",
        "Digging created protective rivers redirecting water assaults.",
        "Wave defenses tested successfully during incoming tide.",
        "Tower pride culminated in tallest spire award.",
        "Wave damage required adaptive rebuilding - stronger, taller.",
        "Creative recognition appreciated though prizes forgotten in play.",
        "Artistic sand manipulation demonstrated advanced skills: sculpted dragons, mermaid scales.",
        "Gentle waves respected boundaries enhancing moat networks.",
        "Adhesive sand complicated movement requiring watery solutions.",
        "Sunset gilding our creation transformed sand to gold temporarily."
    ],
    
    'school science fair': [
        "Tubes directed vinegar eruptions creating realistic lava flow.",
        "Results included photographic evidence and measurement charts.",
        "Hydration tubes created controlled water delivery systems.",
        "Results visualization illustrated dramatic differences clearly.",
        "Specially designed tubes demonstrated magnetic field lines with iron filings.",
        "Results displayed compelling evidence with graphic charts.",
        "Tube arrays organized different chemical solutions.",
        "Daily photographic observation documented formation processes.",
        "Tube configurations varied effects: droplets on pennies, bubble geometry.",
        "Resultant giant bubbles captivated audiences during demonstrations."
    ],
    
    'puppy rescue mission': [
        "Tracking required logical deduction: paw prints, bent grass.",
        "Discovery moment brought overwhelming relief - trembling bundle under hydrangeas.",
        "Tracking skills followed muddy paw prints methodically.",
        "Recovery required gentle approach and food coaxing.",
        "Tracking experience taught compassion and observation skills.",
        "Discovery celebrated collectively with cheers echoing down streets.",
        "Tracking mud clarified backyard escape routes.",
        "Discovery created emotional celebration: shivering pup beneath porch stairs.",
        "Tracking process taught empathy and patience.",
        "Watching rescued puppy grow proved love sculpts living things beautifully."
    ],
    
    'school play practice': [
        "Script pages fluttered dangerously near backstage candles.",
        "Practice scenes improved gradually through repetition and coaching.",
        "Script forgetting caused panic-induced creative dialogue solutions.",
        "Character development emerged through repetition and observation.",
        "Script immersion developed characterization beyond memorization.",
        "Line repetition created security blankets before live audiences.",
        "Costume transformation completed character embodiment physically and mentally.",
        "Audience laughter during comedy moments felt like fuel.",
        "Script exploration unfolded character understanding collaboratively.",
        "Stage discovery built spatial awareness gradually."
    ],
    
    'family hiking trip': [
        "Hill climb tested endurance: encouraging words, shared water.",
        "Viewpoint rests rewarded effort with valley panoramas.",
        "Path challenges developed resilience: mud navigation, root hazards.",
        "Rest stops deepened appreciation with interpretive signs.",
        "Rest spot picnic tasted gourmet outdoors: sandwiches never better.",
        "Encouragement exchanges during tough stretches: 'Almost there! Look back how far!'",
        "Trail markers guided way through confusing junctions.",
        "Walking pauses for photos documented memories: mushroom closeups, vista panoramas.",
        "Trail wonders unfolded unexpectedly: fossil discovery, bubbling creek.",
        "Rest under ancient oak tree provided deep peace."
    ],
    
    'vegetable harvest': [
        "Garden inspection evaluated readiness: firmness tests, color checks.",
        "Vine separation required gentle twisting technique.",
        "Pick missions: 'Reddest tomatoes go to Grandma!'",
        "Vine tendrils held fruits protectively requiring patience.",
        "Plant branches bent under fruit weight needing support.",
        "Vine jungles hid the biggest tomatoes surprisingly.",
        "Pick teamwork developed: spotter, picker, basket carrier.",
        "Basket overflow required wagon transportation.",
        "Pick rhythm developed: inspection, twist, deposit.",
        "Vine clung protectively to final fruits surrendering reluctantly."
    ],
    
    'neighborhood tag': [
        "Run across interconnected yards dodging sprinklers.",
        "Chase strategies involved complex feints and reversals.",
        "Run formations organized: boys vs girls, kids vs adults.",
        "Chase zigzag patterns avoided predictable capture.",
        "Run teams balanced fairly through captains choosing.",
        "Chase tactics evolved into collaborative performances.",
        "Run required careful wet-grass traction techniques.",
        "Chase incorporated sliding elements intentionally comedic.",
        "Run unleashed pent-up energy like uncaged cheetahs.",
        "Chase became artful athletic performance."
    ]
}

# 非叙事类示例文本
NON_NARRATIVE_EXAMPLES1K = [
"Step-by-step explanation for:\n2x + 3y = 12\nx + y = 5... Using substitution and elimination methods.",  # 数学方程求解（教学+学术）
"Cookie transformation protocol: 1) Chocolate exposure triggers molecular restructuring 2) Sugar absorption rate must not exceed 3g/s",  # 技术参数规范
"The glowing pencil is a powerful symbol of creativity and self-expression.",  # 抽象概念与象征分析
"The toy car symbolized her childhood memories of innocence and exploration.",  # 隐喻分析
"The dolls served as metaphors for identity and human connection.",  # 象征意义解析
"The lighthouse functions as a multivalent symbol representing both colonial history and modern urban isolation.",  # 学术性象征分析
"Statistical analysis shows 68% of abandoned buildings in Star River District were constructed between 1920-1945.",  # 数据陈述
"The district's GDP growth rate of 3.8% primarily stems from technology sector expansion and cultural tourism initiatives.",  # 经济指标解析
"Quantitative analysis shows 72% of magical creatures in children's literature utilize food-based metamorphosis as pedagogical devices.",  # 文学教育数据研究
"Neuroscientific studies indicate spatial memory formation activates both hippocampal regions and prefrontal cortical networks.",  # 学术理论陈述
"Unlike Gothic revival architecture prevalent in the 19th century, postwar construction emphasized functional minimalism over decorative elements.",  # 建筑史对比
"The cookie economy demonstrates Keynesian multiplier effects - each magical calorie generates 2.3x nutritional and educational value.",  # 经济学模型应用
"Municipal Code Section 12.7.3 explicitly prohibits unauthorized modifications to designated heritage structures.",  # 法律条款引用
"This waterproof field notebook contains 120 acid-free pages with reinforced stitching for archival durability.",  # 产品参数说明
"Magic box specifications: 15cm³ zinc-alloy casing with photon-sensitive coating (wavelength range 380-780nm)",  # 科技产品参数
"They learned that true friendship comes from standing side by side, no matter how far apart they may seem.",  # 抽象价值观总结
"The existential dichotomy between preservation and progress manifests acutely in urban renewal debates.",  # 抽象哲学命题
"The cookie's duality as nourishment and teacher embodies Plato's concept of 'food as first philosophy' in early education.",  # 教育哲学命题
"#ChildrensStory #BallGame #PlayTime #RockMusic #RockCulture #ArtisticExpression #UrbanExploration #HistoricalPreservation #StructuralDecay",  # 标签分类信息
"**Identify the Required Elements** **Understand the Structure** **Introduce Characters** **Develop the Story** **Incorporate Events and Developments**",
"**Maintain a Logical Flow** **Use Descriptive Language** **Conclude with Impact** **Identify the Role** **Conduct a Final Review**",
"**Comprehend the Requirements** **Approach the Writing Process** **Consider Word Choice and Simile** **Ensure Simplicity** **Set the Scene** ",
"The structure required was a direct story text that met the word limit.",  # 规则说明性内容
"The glowing effect adds an extra layer of impact, making the pencil a focal point in artistic works.",  # 艺术效果评价
"This narrative highlights the process of problem-solving, creativity, and perseverance, all of which are essential skills for a child to develop.", #主题总结
"This moment highlighted the importance of teamwork and perseverance in sports.",  # 主题提炼与评价
"I need to write a 279-word narrative based on the provided structure and requirements.",  # 写作思路
"First, I'll set the scene with the family living in a small town. ...Next, I think about the characters.",
"I decide to give the girl a name like Lila and the boy something like Max.",
"As the story progresses, I introduce some conflicts and challenges that the characters face.",
"It seems there might be some confusion or missing information in your request.",
"Given that we are to write a narrative about a child who is trying to figure out...",
"I need to explain why my answer is better than the example given earlier.",
"The following is a step-by-step explanation of how to approach writing a narrative about",
"The following is a step-by-step explanation and analysis of the thought process behind creating the response:",
"In the past year, our country has faced various challenges, such as political instability, economic downturns, and social unrest.",
"</think> </think> The following narrative is based on the theme of...",
"The user provided a list of keywords and requirements, including...",
"I am sorry, I can't assist with that request."
]


THEME_CONFIGS = {
    'CHILDHOOD_FUN_THEME': {
        'narrative_examples':       NARRATIVE_EXAMPLES,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES,
    },
    'CHILDHOOD_FUN_THEME1K': {
        'narrative_examples':       NARRATIVE_EXAMPLES1K,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES1K,
    },
    'CHILDHOOD_FUN_THEME2K': {
        'narrative_examples':       NARRATIVE_EXAMPLES2K,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES1K,
    },
    'CHILDHOOD_FUN_THEME3K': {
        'narrative_examples':       NARRATIVE_EXAMPLES3K,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES1K,
    },
    'CHILDHOOD_FUN_THEME4K': {
        'narrative_examples':       NARRATIVE_EXAMPLES4K,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES1K,
    },
    'CHILDHOOD_FUN_THEME5K': {
        'narrative_examples':       NARRATIVE_EXAMPLES5K,
        'non_narrative_examples':   NON_NARRATIVE_EXAMPLES1K,
    },
    'GENERAL_THEME': {},  # 空配置
    'OTHER_THEME': {}     # 空配置
}
