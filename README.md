# bg3-animation-remapper
A tool for Baldur's Gate 3 modding that helps with remapping animations to visual object keys!

## How to Use
1. Make sure you have [Python](https://www.python.org/downloads/) installed.
2. Download and then extract the release of this tool into your mod's root directory.
3. Open a command line and navigate it into the same root directory.
4. Execute `pip install -r requirements.txt`
5. Edit `animationKeyRemapper.py` and alter the constants at the top of the file
   - `NEW_RESOURCE_NAME` You can use whatever name you want, but it's nice to make it the name of the animation that you're adding/modifying.
   - `DIRECTORY_FOR_MODDING` This should be a path from the root folder (excluding it) down to a directory with all the files you want to read data from
      (all the .lsx files that you want to add animation data mapping to. Note that this directory can contain further sub-directories. Those
      directories will also be walked through.)
   - `ANIMATION_PRIORITIES_FILE_PATH` This path should lead directly to the file `AnimationSetPriorities.lsx`. This file contains the priority data
      for individual Dynamic Animation Tags.
   - `PRIORITY` Set this to a normal number. The lower the number, the HIGHER the priority (ik Larian Studios named their fields weird as well so
      don't blame me for not calling it something like "`INVERSE_PRIORITY`"). The priority of an animation set determines which animation set to
      prepare/reference when calling a certain animation ID. The reason it's important to have a priority is because sometimes depending on a dynamic
      status a character has, they might have to perform different animations depending on what tags/statuses they have. For example: Barbarian Rage.
      Their idle combat stance is quite different from their normal default combat idle stance. But the engine simply calls to play 'default idle combat'.
      The .lsx files here must figure out which specific animation to play based on many things like Rage, Race, Class, Background, etc...
   - `KEY_REPLACEMENT_MAP` Ok this one is a bit complicated but is also CRUCIAL.  
      This is a list of 3-tuples. The first element in a tuple is the animation ID that the engine will call that you want to 'intercept'.
      For example, this could be like the dodging animation whenever an attack misses you. The generic 'character dodge' animation key.
      The second element in the tuple is the animation subset key that this tuple should belong to. These subset keys are a bit complicated.  
      But essentially these keys are the identifiers that the engine uses to map specific animations to the generic ones. For example, `Wielding a two-handed sword` is one.  
      Lastly, the third element in this tuple is the specific animation you want all of that to map to. for example: `Combat_1HS_REAC_Dodge_F_01.gr2`
      So if the engine calls for the first element animation, and the character set to perform it has the second element map key, then you want it to
      perform the third element specific animation.  
      You can have as many tuples as you want in this list, and the tool will take care of it all.  
      Note that all the elements are UUIDs.
   - `SHOULD_DELETE_PARSED_FILES` This flag can be set to `True` or `False`. If `True`, it will delete the file it obtained the animation data
      from, after it finished generating the added file for that character.
6. Run the script with no arguments (`python ./animationKeyRemapper.py`). **This will do all the annoying work for you and print out your Dynamic Animation Tag
   for you to copy and paste wherever you wish to use it** (typically you'd use it in a status definition)!

For an example of a mod that used this, I used it for my own mod "[Bliss (Block n' Miss Differentiation)](https://www.nexusmods.com/baldursgate3/mods/9646)", which you can download the .pak for and unpack it
to view the source of it. I have left the constants to how they are with that mod in the script uploaded here so you can try to follow along if you wish, and also
because it's easy for me lol because it both shows how to properly format the constants, as well as what they should look similar to.

If you have any questions on how to use it still, then feel free to contact me through DM on Discord (thewhirlwind9) :)
