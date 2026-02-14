# Video Script: Building AI-Powered Dynamic NFTs on GenLayer
## 15-Minute Tutorial Video

**Target Audience:** Developers interested in NFTs and AI  
**Goal:** Teach them to build dynamic NFTs from scratch  
**Tone:** Enthusiastic, educational, approachable

---

## 🎬 INTRO (0:00 - 1:30)

### [SCREEN: Title card with music]

**VISUAL:** Animated NFT morphing colors

**VOICEOVER:**
"What if your NFT could change? Not just once, but continuously - evolving based on real-world events like Bitcoin's price, the weather, or even Twitter sentiment?"

**[CUT TO: Talking head]**

**ON CAMERA:**
"Hey everyone! I'm [NAME], and today I'm going to show you something really cool. We're building an NFT that literally transforms itself based on Bitcoin's price. When BTC goes up, your NFT gets rarer. When it crashes, your NFT turns red. It's like having a living, breathing digital asset."

**[B-ROLL: Quick demo of NFT changing]**

"And the best part? We're doing this on GenLayer - a blockchain that gives smart contracts AI superpowers. No centralized oracles, no complex integrations. Just pure AI magic."

**[SCREEN: Chapter markers appear]**

"In the next 15 minutes, you'll learn:
- What dynamic NFTs are
- How to build one from scratch
- How to integrate AI for real-world data
- And we'll deploy and test it live"

"Let's dive in!"

---

## 📚 CONCEPT EXPLANATION (1:30 - 3:30)

**[SCREEN: Split screen - static vs dynamic NFT]**

**VOICEOVER:**
"First, let's understand what makes an NFT 'dynamic.'"

**[ANIMATION: Static NFT on left, dynamic on right]**

"Traditional NFTs are like photographs - they're frozen in time. Once minted, they never change. The monkey stays a monkey. The punk stays a punk."

**[Dynamic NFT side starts morphing]**

"But dynamic NFTs? They're alive. They can update their metadata, change their appearance, and evolve based on triggers."

**[SCREEN: Use case examples]**

**EXAMPLES SHOWN:**
1. Gaming character leveling up
2. Stock portfolio NFT showing live value
3. Weather-based art changing with seasons

"Why does this matter? Because NFTs become actually useful. Not just collectibles, but functional tools."

**[SCREEN: Our example]**

**ON CAMERA:**
"Today, we're building an NFT tied to Bitcoin's price. Watch what happens..."

**[DEMO: NFT transforming as price changes]**

- **BTC at $30k:** Red, Common, Slow animation
- **BTC at $50k:** Yellow, Rare, Medium animation  
- **BTC at $70k:** Gold, Legendary, Fast animation

"Every attribute - color, rarity, animation - changes automatically. No manual updates needed."

---

## 🏗️ ARCHITECTURE WALKTHROUGH (3:30 - 5:00)

**[SCREEN: Architecture diagram]**

**DIAGRAM SHOWS:**
```
[User] → [Contract] → [AI Oracle] → [Bitcoin APIs]
  ↓         ↓            ↓
Mint    Generate     Fetch Price
Update  Attributes   Consensus
```

**VOICEOVER:**
"Here's how it works at a high level:"

**[ANIMATION: Data flow]**

"Step 1: User mints an NFT
Step 2: Contract asks AI 'what's Bitcoin's price?'
Step 3: AI queries real APIs like CoinGecko
Step 4: Multiple validators reach consensus
Step 5: Contract generates attributes based on price
Step 6: NFT is minted with dynamic attributes"

**[HIGHLIGHT: AI part]**

"The magic is here - GenLayer's AI. It can make HTTP requests, parse responses, and bring real-world data on-chain. No centralized oracles. No API keys in your contract. Just AI."

---

## 💻 CODE WALKTHROUGH (5:00 - 10:00)

**[SCREEN: Code editor open]**

**ON CAMERA:**
"Alright, let's build this! I'll walk you through the key parts, then we'll deploy and test."

### PART 1: Contract Setup (5:00 - 6:00)

**[CODE: Contract initialization]**

```python
class DynamicNFT(gl.Contract):
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.nfts = {}  # All NFT data
        self.owners = {}  # Ownership
        self.last_btc_price = 0  # Cache
```

**VOICEOVER:**
"We start with a standard contract structure. We're storing NFT data in a dictionary, tracking owners, and caching the last known Bitcoin price to reduce AI calls."

### PART 2: AI Integration (6:00 - 7:30)

**[CODE: _fetch_btc_price function]**

```python
def _fetch_btc_price(self) -> int:
    prompt = """Get current Bitcoin price in USD.
    Return only the integer price."""
    
    def fetch():
        return gl.exec_prompt(prompt)
    
    price_str = gl.eq_principle_strict_eq(fetch)
    return int(price_str)
```

**ON CAMERA:**
"This is where AI comes in. We give it a prompt - 'get Bitcoin's price' - and GenLayer's AI actually goes out to the internet, queries price APIs, and brings back the data."

**[HIGHLIGHT: Consensus]**

"Notice `gl.eq_principle_strict_eq` - this means all validators must agree on the price. It's not just one AI answering, it's multiple reaching consensus. That's how we ensure accuracy."

### PART 3: Attribute Generation (7:30 - 8:30)

**[CODE: _generate_attributes function]**

```python
def _generate_attributes(self, btc_price: int):
    if btc_price < 30000:
        color = "Red"
        rarity = "Common"
    elif btc_price < 60000:
        color = "Yellow"
        rarity = "Rare"
    else:
        color = "Gold"
        rarity = "Legendary"
```

**VOICEOVER:**
"Here's the logic that makes NFTs dynamic. We map price ranges to attributes. Higher price = rarer NFT. Simple but powerful."

**[ANIMATION: Price ranges and attributes]**

"You can customize these ranges however you want. The key is making them meaningful - users should feel rewarded when Bitcoin pumps!"

### PART 4: Mint Function (8:30 - 9:30)

**[CODE: mint function]**

```python
@gl.public.write
def mint(self, to_address: str):
    self.total_supply += 1
    token_id = f"NFT-{self.total_supply:04d}"
    
    current_price = self._fetch_btc_price()  # AI call!
    attributes = self._generate_attributes(current_price)
    
    self.nfts[token_id] = {
        "token_id": token_id,
        "owner": to_address,
        "attributes": attributes
    }
```

**ON CAMERA:**
"When someone mints, we fetch the current price, generate attributes, and save everything. Each NFT is born with attributes matching the market at that moment."

### PART 5: Update Function (9:30 - 10:00)

**[CODE: update_nft function]**

```python
@gl.public.write
def update_nft(self, token_id: str):
    new_price = self._fetch_btc_price()
    old_attributes = self.nfts[token_id]["attributes"]
    new_attributes = self._generate_attributes(new_price)
    
    self.nfts[token_id]["attributes"] = new_attributes
    # Show what changed
```

**VOICEOVER:**
"And this is what makes it dynamic - the update function. It refetches the price, recalculates attributes, and updates the NFT. Your Red Common NFT becomes a Gold Legendary as Bitcoin moons!"

---

## 🚀 LIVE DEMO (10:00 - 13:00)

**[SCREEN: GenLayer Studio]**

**ON CAMERA:**
"Alright, theory done. Let's see this in action!"

### Deploy (10:00 - 11:00)

**[SCREEN RECORD: Deployment process]**

**STEPS SHOWN:**
1. Open GenLayer Studio
2. Paste contract code
3. Deploy with name "BitcoinVibes"
4. Contract address appears

**VOICEOVER:**
"Deploying is straightforward. Paste your code, give it a name, hit deploy. In a few seconds, we have a live contract."

### Mint NFT (11:00 - 11:45)

**[SCREEN: Calling mint function]**

**CALL:**
```
contract.mint("my-address")
```

**RESPONSE:**
```
✅ Minted NFT-0001
Initial BTC Price: $47,523
Attributes: {
  color: "Yellow",
  rarity: "Uncommon",
  mood: "Optimistic"
}
```

**ON CAMERA:**
"Boom! NFT minted. Notice it captured the current Bitcoin price - $47,523 - and generated attributes accordingly. Yellow and Uncommon because we're in the mid-range."

### View NFT (11:45 - 12:15)

**[SCREEN: get_nft call]**

**CALL:**
```
contract.get_nft("NFT-0001")
```

**SHOWS:**
- Full metadata
- All attributes
- Creation timestamp
- Owner

**VOICEOVER:**
"We can view the full metadata. This follows standard NFT format, so it's compatible with wallets and marketplaces."

### Update NFT (12:15 - 13:00)

**[SCREEN: update_nft call]**

**CALL:**
```
contract.update_nft("NFT-0001")
```

**RESPONSE:**
```
🔄 Updated NFT-0001
Bitcoin Price: $47,523 → $52,891 (+11.29%)

Attribute Changes:
color: Yellow → Green
rarity: Uncommon → Rare
mood: Optimistic → Bullish
```

**ON CAMERA:**
"And here's the magic! Bitcoin went up, and our NFT automatically evolved. Yellow became Green. Uncommon became Rare. The NFT literally transformed!"

**[B-ROLL: Side by side comparison of before/after]**

---

## 💡 ADVANCED IDEAS (13:00 - 14:00)

**[SCREEN: Concept slides]**

**ON CAMERA:**
"Now that you know how to build this, here are some ideas to take it further:"

**IDEA 1: Multi-Asset NFTs**
[Visual: NFT with BTC + ETH]
"Track multiple cryptocurrencies. Size from Bitcoin, color from Ethereum, rarity from total market cap."

**IDEA 2: Weather-Based Art**
[Visual: NFT changing with weather]
"Create generative art that shifts with the weather in your city. Rainy = dark palette. Sunny = bright colors."

**IDEA 3: Gaming Characters**
[Visual: Character leveling up]
"Character NFTs that gain XP and level up based on gameplay. Stats stored on-chain, updated after battles."

**IDEA 4: Real Estate NFTs**
[Visual: Property token]
"NFTs representing properties that update with market value, rental income, and maintenance records."

**VOICEOVER:**
"The possibilities are endless. Any real-world data can become a trigger for your NFT."

---

## 🎓 WRAP UP (14:00 - 15:00)

**[SCREEN: Key takeaways]**

**ON CAMERA:**
"Let's recap what we built today:"

**CHECKLIST APPEARS:**
- ✅ Dynamic NFT contract
- ✅ AI-powered price oracle
- ✅ Automatic attribute updates
- ✅ Real-world data integration
- ✅ Deployed and tested

"You now know how to create NFTs that actually DO something. That respond to the real world. That evolve and change."

**[SCREEN: Links]**

"All the code is linked below. Full tutorial, contract code, and documentation."

**RESOURCES SHOWN:**
- GitHub Repo
- Written Tutorial
- Discord Community
- GenLayer Docs

**ON CAMERA:**
"If you build something with this, I'd love to see it! Tag me on Twitter, share in the GenLayer Discord, or drop a comment below."

**[SCREEN: Subscribe animation]**

"If you found this helpful, smash that subscribe button. I'm creating more GenLayer tutorials covering DeFi, DAOs, and advanced AI integrations."

**[OUTRO MUSIC]**

"Thanks for watching, and happy building! 🚀"

**[END SCREEN: 15:00]**

---

## 📝 EDITING NOTES

### B-Roll Needed:
- NFT morphing animation
- Code typing shots
- GenLayer Studio interface
- Price charts
- Multiple NFT variations

### Graphics Needed:
- Architecture diagram
- Price range chart
- Attribute mapping table
- Before/after comparisons
- Chapter markers

### Music:
- Upbeat electronic for intro (30s)
- Ambient background for coding sections
- Energetic for live demo
- Outro music (15s)

### Timestamps for YouTube:
```
0:00 - Intro
1:30 - What are Dynamic NFTs?
3:30 - Architecture Overview
5:00 - Code Walkthrough
10:00 - Live Demo
13:00 - Advanced Ideas
14:00 - Wrap Up
```

---

## 🎯 CALL TO ACTION

**In Description:**
```
🔗 LINKS:
📂 Full Code: [GitHub link]
📖 Written Tutorial: [Blog link]
💬 Discord: [Community link]
📚 GenLayer Docs: [Docs link]

⭐ If this helped, please:
- Star the GitHub repo
- Share with fellow developers
- Join our Discord community

🚀 Next Video: Building a Prediction Market with AI
```

**Pinned Comment:**
```
What dynamic NFT would YOU build? Drop your ideas below! 

The most creative one gets featured in the next video 👇
```

---

## ✅ PRE-PRODUCTION CHECKLIST

```
□ Script finalized
□ Code tested and working
□ Studio environment set up
□ Screen recording software ready
□ Camera and mic tested
□ B-roll footage captured
□ Graphics created
□ Music licensed
□ Thumbnails designed (3 variations)
□ YouTube description written
□ Social media posts scheduled
```

---

**Video Title Ideas:**
1. "Build NFTs That EVOLVE (AI-Powered Dynamic NFTs Tutorial)"
2. "Your NFT Can Change - Here's How to Build It"
3. "Dynamic NFTs on GenLayer - Complete Tutorial"

**Thumbnail Concepts:**
1. Split screen: Static NFT → Dynamic NFT
2. NFT with "EVOLVES" text and arrows
3. Bitcoin logo + NFT transforming

---

**Total Runtime:** 14-15 minutes  
**Editing Time:** 3-4 hours  
**Target Upload:** Within 1 week of filming

**Video Script v1.0**
