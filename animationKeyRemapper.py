from lxml import etree
import os
import uuid
from shutil import rmtree

#-MODIFY-CONSTANTS-BELOW-THIS-LINE-----------------------------------------------------------------------------------
NEW_RESOURCE_NAME = "Block_Base"
DIRECTORY_FOR_MODIFYING = "Public\\Block-Miss-Differentiation\\Content\\Assets\\Characters"
ANIMATION_PRIORITIES_FILE_PATH = "Public\\Block-Miss-Differentiation\\AnimationOverrides\\AnimationSetPriorities.lsx"
PRIORITY = 0 # Lower is higher priority. For reference: Race anims priority 20. Class anims priority 10. Githyanki parry anims priority 1. Rage anims priority 0.
KEY_REPLACEMENT_MAP = [ # (<VisualObject_MapKey>, <Animation_SubSet>, <Animation>)
    ("881e6512-732b-48d1-9606-e235bcf97e50", "fcc344b8-b7f1-4b4f-be1d-2267ad7a040c", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "ac3f0da3-0af0-4637-8d5a-06ea063e0860", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "808afd36-6e32-4b3f-a762-bdfb53bc8d52", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "fbddf847-9b06-4913-aca1-38932d01fe60", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "f6fa9d34-e804-4dd2-819b-5fbc9bcd8364", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "f709f223-f46c-44ff-8212-87ca9a2aa5dd", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "8ec7e57c-d445-43de-8606-db413bc8a6da", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "c8082637-b99d-4c3e-b235-8ef902ce1bea", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "9f6580cf-20d4-4603-a80b-47ae036bae59", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "b9c982a6-27a5-4f46-9ad0-7a08f41d2385", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "32bbe70b-19ef-4ca2-9bc9-7beef24c06e0", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "7d722c10-83dd-4c67-96df-6103c88ab593", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "406b8be4-c409-441f-9335-e6b719770949", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "3a08ada3-1499-4fcd-b714-53b1691a549c", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "8c360b6c-0d4b-48be-bc94-a6ac7c8b5a52", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "56ca5794-fd29-4a52-90fc-fc0ba54a06ed", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "e5090d4e-e4d0-46ea-925e-a1d3f78ac6b7", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "3bfdfbfe-4bc4-45c9-b663-400555d13eb4", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "0b503a44-3e2c-4499-9f10-6f7d9f6c12fc", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "c9521594-0e07-43d9-b6d1-e76272b2b2ad", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "ce24030f-8351-4c47-b46d-0c45f2f6e2f5", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "0ed1b9c4-6dd7-4a92-be99-d2ccee0d21c5", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "f2ac8a18-8381-4b99-be9b-cc8f92590c13", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "4a5c721d-8478-4d2d-bb27-982bff9c8f68", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "1323327e-d6f9-4f5f-9408-a01d64ed777a", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("881e6512-732b-48d1-9606-e235bcf97e50", "1a1b8d62-6b9a-477d-8e07-3c4ac65f13d9", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "fcc344b8-b7f1-4b4f-be1d-2267ad7a040c", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "ac3f0da3-0af0-4637-8d5a-06ea063e0860", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "808afd36-6e32-4b3f-a762-bdfb53bc8d52", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "fbddf847-9b06-4913-aca1-38932d01fe60", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "f6fa9d34-e804-4dd2-819b-5fbc9bcd8364", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "f709f223-f46c-44ff-8212-87ca9a2aa5dd", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "8ec7e57c-d445-43de-8606-db413bc8a6da", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "c8082637-b99d-4c3e-b235-8ef902ce1bea", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "9f6580cf-20d4-4603-a80b-47ae036bae59", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "b9c982a6-27a5-4f46-9ad0-7a08f41d2385", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "32bbe70b-19ef-4ca2-9bc9-7beef24c06e0", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "7d722c10-83dd-4c67-96df-6103c88ab593", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "406b8be4-c409-441f-9335-e6b719770949", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "3a08ada3-1499-4fcd-b714-53b1691a549c", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "8c360b6c-0d4b-48be-bc94-a6ac7c8b5a52", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "56ca5794-fd29-4a52-90fc-fc0ba54a06ed", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "e5090d4e-e4d0-46ea-925e-a1d3f78ac6b7", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "3bfdfbfe-4bc4-45c9-b663-400555d13eb4", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "0b503a44-3e2c-4499-9f10-6f7d9f6c12fc", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "c9521594-0e07-43d9-b6d1-e76272b2b2ad", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "ce24030f-8351-4c47-b46d-0c45f2f6e2f5", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "0ed1b9c4-6dd7-4a92-be99-d2ccee0d21c5", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "f2ac8a18-8381-4b99-be9b-cc8f92590c13", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "4a5c721d-8478-4d2d-bb27-982bff9c8f68", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "1323327e-d6f9-4f5f-9408-a01d64ed777a", "7a3aa912-815f-a705-2a83-7f82780bc4d6"),
    ("5dcdcc4c-3744-451f-b5cf-ed96664481cc", "1a1b8d62-6b9a-477d-8e07-3c4ac65f13d9", "7a3aa912-815f-a705-2a83-7f82780bc4d6")
]

SHOULD_DELETE_PARSED_FILES = True
#-DO-NOT-MODIFY-ANY-CODE-BELOW-THIS-LINE-UNLESS-YOU-REALLY-KNOW-WHAT-YOU'RE-DOING------------------------------------

dynamic_animation_tag = ""
list_of_affected_characters = []

def _insert_block_animation(root_parent_element, animation_uuid, animation_subset_key, object_key):
    animation_element = None
    resource_id = uuid.uuid4()
    block_root_element = None
    for element in root_parent_element:
        if element.get("id") == "Resource":
            for sub_element in element:
                if sub_element.get("value") == NEW_RESOURCE_NAME:
                    block_root_element = element
                    break
        if block_root_element is not None: break

    if block_root_element is None: # If you haven't created the element yet.
        block_root_element = etree.SubElement(root_parent_element, "node")
        block_root_element.set("id", "Resource")

        id_element = etree.SubElement(block_root_element, "attribute")
        id_element.set("id", "ID")
        id_element.set("type", "FixedString")
        id_element.set("value", str(resource_id))
        name_element = etree.SubElement(block_root_element, "attribute")
        name_element.set("id", "Name")
        name_element.set("type", "LSString")
        name_element.set("value", str(NEW_RESOURCE_NAME))
        preview_element = etree.SubElement(block_root_element, "attribute")
        preview_element.set("id", "PreviewVisualResourceID")
        preview_element.set("type", "guid")
        preview_element.set("value", "00000000-0000-0000-0000-000000000000")
        source_file_element = etree.SubElement(block_root_element, "attribute")
        source_file_element.set("id", "SourceFile")
        source_file_element.set("type", "LSString")
        source_file_element.set("value", "")
        original_file_element = etree.SubElement(block_root_element, "attribute")
        original_file_element.set("id", "_OriginalFileVersion_")
        original_file_element.set("type", "int64")
        original_file_element.set("value", "144115205255725665")
        parent_element_1 = etree.SubElement(block_root_element, "children")
        animation_set_element = etree.SubElement(parent_element_1, "node")
        animation_set_element.set("id", "AnimationSet")
        parent_element_2 = etree.SubElement(animation_set_element, "children")
        animation_bank_element = etree.SubElement(parent_element_2, "node")
        animation_bank_element.set("id", "AnimationBank")
        short_name_element = etree.SubElement(animation_bank_element, "attribute")
        short_name_element.set("id", "ShortNameSetId")
        short_name_element.set("type", "guid")
        short_name_element.set("value", "00000000-0000-0000-0000-000000000000")
        parent_element_3 = etree.SubElement(animation_bank_element, "children")
        animation_subsets_element = etree.SubElement(parent_element_3, "node")
        animation_subsets_element.set("id", "AnimationSubSets")
        parent_element_4 = etree.SubElement(animation_subsets_element, "children")

        object_element = etree.SubElement(parent_element_4, "node")
        object_element.set("id", "Object")
        fallback_subset_element = etree.SubElement(object_element, "attribute")
        fallback_subset_element.set("id", "FallBackSubSet")
        fallback_subset_element.set("type", "FixedString")
        fallback_subset_element.set("value", "")
        map_key_subset_element = etree.SubElement(object_element, "attribute")
        map_key_subset_element.set("id", "MapKey")
        map_key_subset_element.set("type", "FixedString")
        map_key_subset_element.set("value", str(animation_subset_key))
        parent_element_5 = etree.SubElement(object_element, "children")
        animation_element = etree.SubElement(parent_element_5, "node")
        animation_element.set("id", "Animation")
        parent_element_6 = etree.SubElement(animation_element, "children")

        animation_object_element = etree.SubElement(parent_element_6, "node")
        animation_object_element.set("id", "Object")
        animation_id_element = etree.SubElement(animation_object_element, "attribute")
        animation_id_element.set("id", "ID")
        animation_id_element.set("type", "FixedString")
        animation_id_element.set("value", str(animation_uuid))
        animation_map_key_element = etree.SubElement(animation_object_element, "attribute")
        animation_map_key_element.set("id", "MapKey")
        animation_map_key_element.set("type", "FixedString")
        animation_map_key_element.set("value", str(object_key))
    else:
        resource_id = block_root_element[0].get("value")
        animation_subsets = None
        subset_object_element = None
        for element in block_root_element.iterdescendants():
            if element.get("id") == "AnimationSubSets":
                animation_subsets = element[0]
                break
        for subset in animation_subsets:
            if subset[1].get("id") != "MapKey":
                print(f"ERROR in parsing lsx. Expected MapKey as id. Got {subset[1].get('id')} instead. Aborting script")
                exit(1)
            if subset[1].get("value") == str(animation_subset_key):
                subset_object_element = subset
                break

        if subset_object_element is None:
            object_element = etree.SubElement(animation_subsets, "node")
            object_element.set("id", "Object")
            fallback_subset_element = etree.SubElement(object_element, "attribute")
            fallback_subset_element.set("id", "FallBackSubSet")
            fallback_subset_element.set("type", "FixedString")
            fallback_subset_element.set("value", "")
            map_key_subset_element = etree.SubElement(object_element, "attribute")
            map_key_subset_element.set("id", "MapKey")
            map_key_subset_element.set("type", "FixedString")
            map_key_subset_element.set("value", str(animation_subset_key))
            parent_element_5 = etree.SubElement(object_element, "children")
            animation_element = etree.SubElement(parent_element_5, "node")
            animation_element.set("id", "Animation")
            parent_element_6 = etree.SubElement(animation_element, "children")

            animation_object_element = etree.SubElement(parent_element_6, "node")
            animation_object_element.set("id", "Object")
            animation_id_element = etree.SubElement(animation_object_element, "attribute")
            animation_id_element.set("id", "ID")
            animation_id_element.set("type", "FixedString")
            animation_id_element.set("value", str(animation_uuid))
            animation_map_key_element = etree.SubElement(animation_object_element, "attribute")
            animation_map_key_element.set("id", "MapKey")
            animation_map_key_element.set("type", "FixedString")
            animation_map_key_element.set("value", str(object_key))
        else:
            animation_element = subset_object_element
            for ele in subset_object_element.iterdescendants():
                if ele.get("id") == "Animation":
                    animation_element = ele[0]
                    break
            duplicate_animation = False
            for ele in animation_element.iterdescendants():
                if ele.get("id") == "MapKey" and ele.get("value") == str(object_key):
                    duplicate_animation = True
                    break
            if not duplicate_animation:
                animation_object_element = etree.SubElement(animation_element, "node")
                animation_object_element.set("id", "Object")
                animation_id_element = etree.SubElement(animation_object_element, "attribute")
                animation_id_element.set("id", "ID")
                animation_id_element.set("type", "FixedString")
                animation_id_element.set("value", str(animation_uuid))
                animation_map_key_element = etree.SubElement(animation_object_element, "attribute")
                animation_map_key_element.set("id", "MapKey")
                animation_map_key_element.set("type", "FixedString")
                animation_map_key_element.set("value", str(object_key))

    return resource_id

def _insert_block_animation_override(new_animation_set_override_element, resource_id):
    global dynamic_animation_tag
    new_animation_set_override_element.set("id", "AnimationSetOverrides")
    pair_element_1 = etree.SubElement(new_animation_set_override_element, "attribute")
    pair_element_1.set("id", "PairElement1")
    pair_element_1.set("type", "guid")
    pair_element_1.set("value", str(dynamic_animation_tag))
    pair_element_2 = etree.SubElement(new_animation_set_override_element, "attribute")
    pair_element_2.set("id", "PairElement2")
    pair_element_2.set("type", "FixedString")
    pair_element_2.set("value", str(resource_id))
    override_type_element = etree.SubElement(new_animation_set_override_element, "attribute")
    override_type_element.set("id", "strAnimationSetOverrideType")
    override_type_element.set("type", "int32")
    override_type_element.set("value", "0")

def recurse_through_directory(root_path, total_files):
    global list_of_affected_characters
    curr_file_num = 0
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            curr_file_num += 1
            resource_id = ""
            modified_file = False
            file_path = os.path.join(root, file_name)
            if file_path.endswith(".lsx"):
                print(f"\r\033[KGenerating files... {round((curr_file_num / total_files) * 100)}% complete", end="")
                tree = etree.parse(file_path)
                reading_root = tree.getroot()
                for element in reading_root:
                    if element.get("id") == "AnimationSetBank":
                        reading_root = element[0]
                        break
                if reading_root != tree.getroot():
                    for remapping in KEY_REPLACEMENT_MAP:
                        resource_id = _insert_block_animation(reading_root[0], remapping[2], remapping[1], remapping[0])
                        if resource_id != "":
                            modified_file = True
                            if file_path not in list_of_affected_characters: list_of_affected_characters.append(file_path)
                if modified_file:
                    writing_root = etree.Element("save")
                    animation_set_bank_region_element = etree.SubElement(writing_root, "region")
                    animation_set_bank_region_element.set("id", "AnimationSetBank")
                    animation_set_bank_region_element.append(reading_root)
                    
                    reading_root = tree.getroot()
                    visual_bank_element = None
                    for element in reading_root.iterdescendants():
                        if element.tag == "node" and element.get("id") == "VisualBank":
                            visual_bank_element = element
                            for resource in element[0]:
                                if resource.get("id") == "Resource":
                                    for resource_child in resource:
                                        if resource_child.tag == "children":
                                            new_animation_set_override_element = etree.SubElement(resource_child, "node")
                                            _insert_block_animation_override(new_animation_set_override_element, resource_id)
                                            break
                                    
                            break
                    
                    if visual_bank_element is not None:
                        visual_bank_region_element = etree.SubElement(writing_root, "region")
                        visual_bank_region_element.set("id", "VisualBank")
                        visual_bank_region_element.append(visual_bank_element)
                    etree.ElementTree(writing_root).write(root + f"\\{NEW_RESOURCE_NAME}.lsf.lsx", pretty_print=True, xml_declaration=True, encoding="utf-8")
                
            if SHOULD_DELETE_PARSED_FILES:
                os.remove(file_path)
                try: os.removedirs(root)
                except: pass


def update_animation_set_priorities(animation_priorities_path, animation_name, priority):
    global dynamic_animation_tag
    tree = etree.parse(animation_priorities_path)
    root = tree.getroot()
    for element in root.iterdescendants():
        if element.tag == "children":
            new_animation_set_priority_element = etree.SubElement(element, "node")
            new_animation_set_priority_element.set("id", "AnimationSetPriority")
            name_element = etree.SubElement(new_animation_set_priority_element, "attribute")
            name_element.set("id", "Name")
            name_element.set("type", "LSString")
            name_element.set("value", str(animation_name))
            priority_element = etree.SubElement(new_animation_set_priority_element, "attribute")
            priority_element.set("id", "Priority")
            priority_element.set("type", "int32")
            priority_element.set("value", str(priority))
            uuid_element = etree.SubElement(new_animation_set_priority_element, "attribute")
            uuid_element.set("id", "UUID")
            uuid_element.set("type", "guid")
            uuid_element.set("value", str(dynamic_animation_tag))

            break
    
    tree.write(animation_priorities_path, pretty_print=True, xml_declaration=True, encoding="utf-8")

if __name__ == "__main__":
    dynamic_animation_tag = uuid.uuid4()
    num_files = 0
    for root, dirs, files in os.walk(DIRECTORY_FOR_MODIFYING):
        num_files += len(files)
    recurse_through_directory(DIRECTORY_FOR_MODIFYING, num_files)

    update_animation_set_priorities(ANIMATION_PRIORITIES_FILE_PATH, NEW_RESOURCE_NAME, PRIORITY)

    print(f"\r\033[KComplete! Here's your DynamicAnimationTag: {dynamic_animation_tag}")