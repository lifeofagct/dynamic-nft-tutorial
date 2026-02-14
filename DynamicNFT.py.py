# { "Depends": "py-genlayer:test" }
"""
AI-Powered Dynamic NFT
======================

An NFT that changes its metadata based on real-world data using AI.

This contract demonstrates:
- Dynamic NFT metadata
- AI-powered data fetching
- Real-world event integration
- Automated trait updates

Author: HASBUNALLAH AYO ABDULRAHMAN
License: MIT
"""

from genlayer import *


class DynamicNFT(gl.Contract):
    """
    Dynamic NFT that updates based on Bitcoin price.
    
    The NFT's attributes change when BTC crosses certain price thresholds:
    - Color changes based on price range
    - Rarity adjusts with volatility
    - Animation speed tied to market movement
    """
    
    def __init__(self, name: str, symbol: str):
        """Initialize the NFT collection"""
        self.name = name
        self.symbol = symbol
        self.total_supply = 0
        self.nfts = {}  # token_id -> NFT data
        self.owners = {}  # token_id -> owner address
        self.last_btc_price = 0
        self.price_updates = []  # history of price updates
    
    @gl.public.write
    def mint(self, to_address: str) -> str:
        """
        Mint a new Dynamic NFT.
        
        Args:
            to_address: Address to receive the NFT
            
        Returns:
            Token ID of the minted NFT
        """
        
        # Increment token ID
        self.total_supply += 1
        token_id = f"NFT-{self.total_supply:04d}"
        
        # Get current Bitcoin price via AI
        current_price = self._fetch_btc_price()
        
        # Generate initial attributes based on current price
        attributes = self._generate_attributes(current_price)
        
        # Create NFT
        self.nfts[token_id] = {
            "token_id": token_id,
            "owner": to_address,
            "created_at": gl.block_timestamp,
            "last_updated": gl.block_timestamp,
            "creation_price": current_price,
            "attributes": attributes,
            "update_count": 0
        }
        
        self.owners[token_id] = to_address
        self.last_btc_price = current_price
        
        return f"✅ Minted {token_id} to {to_address}\nInitial BTC Price: ${current_price:,}\nAttributes: {attributes}"
    
    @gl.public.write
    def update_nft(self, token_id: str) -> str:
        """
        Update NFT attributes based on current Bitcoin price.
        
        This demonstrates the "dynamic" aspect - the NFT changes!
        
        Args:
            token_id: ID of the NFT to update
            
        Returns:
            Update summary
        """
        
        if token_id not in self.nfts:
            return "ERROR: NFT not found"
        
        nft = self.nfts[token_id]
        
        # Fetch current Bitcoin price
        new_price = self._fetch_btc_price()
        old_price = self.last_btc_price if self.last_btc_price > 0 else nft["creation_price"]
        
        # Calculate price change
        price_change = ((new_price - old_price) / old_price) * 100
        
        # Generate new attributes based on current price
        old_attributes = nft["attributes"].copy()
        new_attributes = self._generate_attributes(new_price)
        
        # Update NFT
        nft["attributes"] = new_attributes
        nft["last_updated"] = gl.block_timestamp
        nft["update_count"] += 1
        
        # Record price update
        self.price_updates.append({
            "timestamp": gl.block_timestamp,
            "price": new_price,
            "change": price_change
        })
        
        self.last_btc_price = new_price
        
        # Generate update summary
        changes = []
        for key in new_attributes:
            if old_attributes.get(key) != new_attributes[key]:
                changes.append(f"{key}: {old_attributes.get(key)} → {new_attributes[key]}")
        
        summary = f"""🔄 Updated {token_id}

Bitcoin Price: ${old_price:,} → ${new_price:,} ({price_change:+.2f}%)

Attribute Changes:
{chr(10).join(changes) if changes else "No changes"}

Total Updates: {nft['update_count']}
"""
        
        return summary
    
    @gl.public.view
    def get_nft(self, token_id: str) -> dict:
        """Get NFT metadata and attributes"""
        
        if token_id not in self.nfts:
            return {"error": "NFT not found"}
        
        nft = self.nfts[token_id]
        
        return {
            "token_id": nft["token_id"],
            "owner": nft["owner"],
            "name": f"{self.name} #{token_id}",
            "description": f"A dynamic NFT that evolves with Bitcoin price movements",
            "image": self._generate_image_url(nft["attributes"]),
            "attributes": nft["attributes"],
            "created_at": nft["created_at"],
            "last_updated": nft["last_updated"],
            "creation_price": nft["creation_price"],
            "update_count": nft["update_count"]
        }
    
    @gl.public.view
    def owner_of(self, token_id: str) -> str:
        """Get owner of an NFT"""
        return self.owners.get(token_id, "Not found")
    
    @gl.public.view
    def get_collection_stats(self) -> dict:
        """Get collection statistics"""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "total_supply": self.total_supply,
            "last_btc_price": self.last_btc_price,
            "total_updates": len(self.price_updates)
        }
    
    # ========================================
    # Private Helper Methods
    # ========================================
    
    def _fetch_btc_price(self) -> int:
        """
        Fetch current Bitcoin price using AI.
        
        In production, this queries real price APIs.
        """
        
        prompt = """Get the current Bitcoin (BTC) price in USD.

Query from reliable sources like CoinGecko or CoinMarketCap.
Return ONLY the price as an integer (no decimals, no text).

Example response: 45000"""
        
        def fetch():
            return gl.exec_prompt(prompt).strip()
        
        try:
            price_str = gl.eq_principle_strict_eq(fetch)
            price = int(price_str)
            
            # Sanity check
            if price < 1000 or price > 1000000:
                raise Exception("Price out of reasonable range")
            
            return price
            
        except:
            # Fallback to last known price
            return self.last_btc_price if self.last_btc_price > 0 else 45000
    
    def _generate_attributes(self, btc_price: int) -> dict:
        """
        Generate NFT attributes based on Bitcoin price.
        
        This is where the "dynamic" magic happens!
        """
        
        # Color based on price range
        if btc_price < 30000:
            color = "Red"
            mood = "Bearish"
        elif btc_price < 45000:
            color = "Orange"
            mood = "Neutral"
        elif btc_price < 60000:
            color = "Yellow"
            mood = "Optimistic"
        elif btc_price < 75000:
            color = "Green"
            mood = "Bullish"
        else:
            color = "Gold"
            mood = "Moon"
        
        # Rarity based on price (higher = rarer)
        if btc_price < 35000:
            rarity = "Common"
        elif btc_price < 50000:
            rarity = "Uncommon"
        elif btc_price < 65000:
            rarity = "Rare"
        elif btc_price < 80000:
            rarity = "Epic"
        else:
            rarity = "Legendary"
        
        # Animation speed based on price (faster when higher)
        if btc_price < 40000:
            animation = "Slow"
        elif btc_price < 60000:
            animation = "Medium"
        else:
            animation = "Fast"
        
        # Background style
        if btc_price < 40000:
            background = "Cloudy"
        elif btc_price < 55000:
            background = "Sunset"
        elif btc_price < 70000:
            background = "Clear Sky"
        else:
            background = "Starry Night"
        
        return {
            "color": color,
            "rarity": rarity,
            "mood": mood,
            "animation_speed": animation,
            "background": background,
            "btc_price": btc_price
        }
    
    def _generate_image_url(self, attributes: dict) -> str:
        """
        Generate image URL based on attributes.
        
        In production, this would generate actual images
        or point to a rendering service.
        """
        
        # Encode attributes in URL
        color = attributes.get("color", "Blue")
        rarity = attributes.get("rarity", "Common")
        animation = attributes.get("animation_speed", "Medium")
        
        # Example URL (in production, use actual image generator)
        return f"https://nft-generator.example.com/generate?color={color}&rarity={rarity}&animation={animation}"
    
    @gl.public.write
    def batch_update_all(self) -> str:
        """
        Update all NFTs in the collection.
        
        Useful for automated updates triggered by external events.
        """
        
        if self.total_supply == 0:
            return "No NFTs to update"
        
        # Fetch current price once
        new_price = self._fetch_btc_price()
        
        updated_count = 0
        for token_id in self.nfts.keys():
            # Update each NFT
            nft = self.nfts[token_id]
            new_attributes = self._generate_attributes(new_price)
            nft["attributes"] = new_attributes
            nft["last_updated"] = gl.block_timestamp
            nft["update_count"] += 1
            updated_count += 1
        
        self.last_btc_price = new_price
        
        return f"✅ Updated {updated_count} NFTs\nCurrent BTC Price: ${new_price:,}"
    
    @gl.public.view
    def preview_update(self, token_id: str) -> dict:
        """
        Preview what attributes would change without actually updating.
        
        Useful for showing users what will happen before they commit.
        """
        
        if token_id not in self.nfts:
            return {"error": "NFT not found"}
        
        nft = self.nfts[token_id]
        
        # Simulate fetching new price (in real implementation, would use AI)
        simulated_price = self.last_btc_price if self.last_btc_price > 0 else 45000
        
        current_attributes = nft["attributes"]
        new_attributes = self._generate_attributes(simulated_price)
        
        changes = {}
        for key in new_attributes:
            if current_attributes.get(key) != new_attributes[key]:
                changes[key] = {
                    "old": current_attributes.get(key),
                    "new": new_attributes[key]
                }
        
        return {
            "token_id": token_id,
            "current_price": simulated_price,
            "would_change": len(changes) > 0,
            "changes": changes
        }
