CREATE TABLE "ability" (
	"id_ability"	INTEGER NOT NULL UNIQUE,
	"ability_name"	TEXT NOT NULL,
	PRIMARY KEY("id_ability" AUTOINCREMENT)
)

CREATE TABLE "adventuring_gear" (
	"id_adventuring_gear"	INTEGER NOT NULL UNIQUE,
	"adventuring_gear_name"	TEXT NOT NULL,
	"adventuring_gear_description"	TEXT,
	"adventuring_gear_type"	INTEGER,
	"adventuring_gear_count"	INTEGER NOT NULL DEFAULT 1,
	"adventuring_gear_cost"	INTEGER NOT NULL DEFAULT 1,
	"adventuring_gear_weight"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_adventuring_gear" AUTOINCREMENT),
	FOREIGN KEY("adventuring_gear_type") REFERENCES "adventuring_gear_type"("id_adventuring_gear_type")
)

CREATE TABLE "adventuring_gear_type" (
	"id_adventuring_gear_type"	INTEGER NOT NULL UNIQUE,
	"adventuring_gear_type_name"	TEXT NOT NULL,
	PRIMARY KEY("id_adventuring_gear_type" AUTOINCREMENT)
)

CREATE TABLE "armors" (
	"id_armors"	INTEGER NOT NULL UNIQUE,
	"armor_enum"	INTEGER NOT NULL,
	"armor_rang"	INTEGER NOT NULL DEFAULT 0,
	"armor_name"	TEXT NOT NULL,
	"armor_description"	TEXT,
	"cost"	INTEGER NOT NULL,
	"armor_class"	INTEGER NOT NULL,
	"dex_modifier"	INTEGER,
	"strenght"	INTEGER NOT NULL DEFAULT 0,
	"stealth"	NUMERIC NOT NULL DEFAULT 0,
	"weight"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id_armors" AUTOINCREMENT)
)

CREATE TABLE "classes" (
	"id_classes"	INTEGER NOT NULL UNIQUE,
	"class_name"	TEXT NOT NULL,
	"class_description"	TEXT NOT NULL,
	"hit_die"	INTEGER NOT NULL DEFAULT 8,
	"primary_ability_count"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_classes" AUTOINCREMENT)
)

CREATE TABLE "equipment_pack" (
	"id_equipment_pack"	INTEGER NOT NULL UNIQUE,
	"equipment_pack_name"	TEXT NOT NULL,
	"equipment_pack_desc"	TEXT,
	"equipment_pack_cost"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_equipment_pack" AUTOINCREMENT)
)

CREATE TABLE "equipment_pack_adventuring_gear" (
	"id_equipment_pack_adventuring_gear"	INTEGER NOT NULL UNIQUE,
	"id_equipment_pack"	INTEGER NOT NULL DEFAULT 1,
	"id_adventuring_gear"	INTEGER NOT NULL DEFAULT 1,
	"count"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_equipment_pack_adventuring_gear" AUTOINCREMENT)
)

CREATE TABLE "preficiencies_armor" (
	"id_preficiencies_armor"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL,
	"id_armors"	INTEGER NOT NULL,
	FOREIGN KEY("id_armors") REFERENCES "armors"("id_armors"),
	PRIMARY KEY("id_preficiencies_armor" AUTOINCREMENT),
	FOREIGN KEY("id_classes") REFERENCES "classes"("id_classes")
)

CREATE TABLE "preficiencies_weapons" (
	"id_preficiencies_weapons"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL,
	"id_weapons"	INTEGER NOT NULL,
	FOREIGN KEY("id_weapons") REFERENCES "weapons"("id_weapons"),
	FOREIGN KEY("id_classes") REFERENCES "classes"("id_classes"),
	PRIMARY KEY("id_preficiencies_weapons" AUTOINCREMENT)
)

CREATE TABLE "primary_ability" (
	"id_primary_ability"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL DEFAULT 1,
	"id_ability"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_primary_ability" AUTOINCREMENT),
	FOREIGN KEY("id_ability") REFERENCES "ability"("id_ability")
)

CREATE TABLE "saves_ability" (
	"id_saves_ability"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL DEFAULT 1,
	"id_ability"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("id_classes") REFERENCES "classes"("id_classes"),
	FOREIGN KEY("id_ability") REFERENCES "ability"("id_ability"),
	PRIMARY KEY("id_saves_ability" AUTOINCREMENT)
)

CREATE TABLE "startup_armors" (
	"id_startup_armors"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL DEFAULT 1,
	"id_armors"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_startup_armors" AUTOINCREMENT),
	FOREIGN KEY("id_classes") REFERENCES "classes"("id_classes"),
	FOREIGN KEY("id_armors") REFERENCES "armors"("id_armors")
)

CREATE TABLE "startup_items" (
	"id_startup_items"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL DEFAULT 1,
	"id_weapons"	INTEGER,
	"id_adventuring_gear"	INTEGER,
	"id_equipment_pack"	INTEGER,
	"count"	INTEGER NOT NULL DEFAULT 1,
	"startup_items_pack"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id_startup_items" AUTOINCREMENT),
	FOREIGN KEY("id_weapons") REFERENCES "weapons"("id_weapons"),
	FOREIGN KEY("id_adventuring_gear") REFERENCES "adventuring_gear"("id_adventuring_gear"),
	FOREIGN KEY("id_equipment_pack") REFERENCES "equipment_pack"("id_equipment_pack")
)

CREATE TABLE "startup_weapons" (
	"id_startup_weapons"	INTEGER NOT NULL UNIQUE,
	"id_classes"	INTEGER NOT NULL DEFAULT 1,
	"id_weapons"	INTEGER NOT NULL DEFAULT 1,
	"off_hand"	NUMERIC NOT NULL DEFAULT 0,
	"pack_id"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("id_classes") REFERENCES "classes"("id_classes"),
	FOREIGN KEY("id_weapons") REFERENCES "weapons"("id_weapons"),
	PRIMARY KEY("id_startup_weapons" AUTOINCREMENT)
)

CREATE TABLE "weapon_damage_type" (
	"id_weapon_damage_type"	INTEGER NOT NULL UNIQUE,
	"weapon_damage_type_name"	TEXT,
	PRIMARY KEY("id_weapon_damage_type" AUTOINCREMENT)
)

CREATE TABLE "weapon_rang" (
	"id_weapon_rang"	INTEGER NOT NULL UNIQUE,
	"weapon_rang_name"	TEXT NOT NULL,
	PRIMARY KEY("id_weapon_rang" AUTOINCREMENT)
)

CREATE TABLE "weapons" (
	"id_weapons"	INTEGER NOT NULL UNIQUE,
	"weapon_enum"	INTEGER NOT NULL,
	"id_weapon_rang"	INTEGER NOT NULL,
	"weapon_name"	TEXT NOT NULL,
	"weapon_description"	TEXT,
	"weapon_cost"	INTEGER NOT NULL DEFAULT 1,
	"damage_quantity"	INTEGER NOT NULL DEFAULT 1,
	"weapon_damage"	INTEGER NOT NULL DEFAULT 4,
	"id_weapon_damage_type"	INTEGER,
	"weapon_weight"	NUMERIC NOT NULL DEFAULT 0.25,
	"light"	NUMERIC NOT NULL DEFAULT 0,
	"heavy"	NUMERIC NOT NULL DEFAULT 0,
	"two_hand"	NUMERIC NOT NULL DEFAULT 0,
	"reach"	NUMERIC NOT NULL DEFAULT 0,
	"finesse"	NUMERIC NOT NULL DEFAULT 0,
	"thrown"	NUMERIC NOT NULL DEFAULT 0,
	"ammunition"	NUMERIC NOT NULL DEFAULT 0,
	"range_from"	INTEGER NOT NULL DEFAULT 0,
	"range_to"	INTEGER NOT NULL DEFAULT 0,
	"versatile"	NUMERIC NOT NULL DEFAULT 0,
	"versatile_value"	INTEGER,
	"loading"	NUMERIC NOT NULL DEFAULT 0,
	"special"	NUMERIC NOT NULL DEFAULT 0,
	FOREIGN KEY("id_weapon_damage_type") REFERENCES "weapon_damage_type"("id_weapon_damage_type"),
	PRIMARY KEY("id_weapons" AUTOINCREMENT),
	FOREIGN KEY("id_weapon_rang") REFERENCES "weapon_rang"("id_weapon_rang")
)


