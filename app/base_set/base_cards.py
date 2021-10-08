from app.models.cards import Treasure, Victory

# Treasures
copper = Treasure(name="Copper", cost=0, money=1)
silver = Treasure(name="Silver", cost=3, money=2)
gold = Treasure(name="Gold", cost=6, money=3)

# Victory
estate = Victory(name="Estate", cost=2, victory_points=1)
duchy = Victory(name="Duchy", cost=5, victory_points=3)
province = Victory(name="Province", cost=8, victory_points=6)
