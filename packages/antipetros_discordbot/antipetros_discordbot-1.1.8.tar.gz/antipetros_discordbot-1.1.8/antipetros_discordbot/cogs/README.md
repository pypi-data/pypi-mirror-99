# Cogs Info


<p align="center"><img src="/art/finished/images/cog_icon.png" alt="Cog_Icon"/></p>


---

## ToC



  
  - [Info](#info)    
    - [AdministrationCog](#administrationcog)        
        - [delete_msg](#__delete_msg__)    
    - [AntistasiLogWatcherCog](#antistasilogwatchercog)        
        - [get_newest_logs](#__get_newest_logs__)        
        - [get_newest_mod_data](#__get_newest_mod_data__)    
    - [BotAdminCog](#botadmincog)        
        - [add_to_blacklist](#__add_to_blacklist__)        
        - [add_who_is_phrase](#__add_who_is_phrase__)        
        - [all_aliases](#__all_aliases__)        
        - [invocation_prefixes](#__invocation_prefixes__)        
        - [life_check](#__life_check__)        
        - [remove_from_blacklist](#__remove_from_blacklist__)        
        - [self_announcement](#__self_announcement__)        
        - [send_log_file](#__send_log_file__)        
        - [tell_uptime](#__tell_uptime__)        
        - [tell_version](#__tell_version__)    
    - [BotFeedbackCog](#botfeedbackcog)    
    - [CommunityServerInfoCog](#communityserverinfocog)        
        - [current_online_server](#__current_online_server__)        
        - [current_players](#__current_players__)        
        - [exclude_from_server_status_notification](#__exclude_from_server_status_notification__)        
        - [undo_exclude_from_server_status_notification](#__undo_exclude_from_server_status_notification__)    
    - [ConfigCog](#configcog)        
        - [add_alias](#__add_alias__)        
        - [change_setting_to](#__change_setting_to__)        
        - [config_request](#__config_request__)        
        - [list_configs](#__list_configs__)        
        - [overwrite_config_from_file](#__overwrite_config_from_file__)        
        - [show_config_content](#__show_config_content__)        
        - [show_config_content_raw](#__show_config_content_raw__)    
    - [FaqCog](#faqcog)        
        - [post_faq_by_number](#__post_faq_by_number__)    
    - [GiveAwayCog](#giveawaycog)        
        - [abort_give_away](#__abort_give_away__)        
        - [create_giveaway](#__create_giveaway__)        
        - [finish_give_away](#__finish_give_away__)    
    - [ImageManipulatorCog](#imagemanipulatorcog)        
        - [add_font](#__add_font__)        
        - [add_stamp](#__add_stamp__)        
        - [available_stamps](#__available_stamps__)        
        - [list_fonts](#__list_fonts__)        
        - [member_avatar](#__member_avatar__)        
        - [stamp_image](#__stamp_image__)        
        - [text_to_image](#__text_to_image__)    
    - [KlimBimCog](#klimbimcog)        
        - [choose_random](#__choose_random__)        
        - [flip_coin](#__flip_coin__)        
        - [make_figlet](#__make_figlet__)        
        - [roll_dice](#__roll_dice__)        
        - [show_user_info](#__show_user_info__)        
        - [the_dragon](#__the_dragon__)        
        - [urban_dictionary](#__urban_dictionary__)    
    - [PerformanceCog](#performancecog)        
        - [get_command_stats](#__get_command_stats__)        
        - [initial_memory_use](#__initial_memory_use__)        
        - [report](#__report__)        
        - [report_latency](#__report_latency__)        
        - [report_memory](#__report_memory__)    
    - [PurgeMessagesCog](#purgemessagescog)        
        - [purge_antipetros](#__purge_antipetros__)    
    - [SaveSuggestionCog](#savesuggestioncog)        
        - [auto_accept_suggestions](#__auto_accept_suggestions__)        
        - [clear_all_suggestions](#__clear_all_suggestions__)        
        - [get_all_suggestions](#__get_all_suggestions__)        
        - [mark_discussed](#__mark_discussed__)        
        - [remove_all_userdata](#__remove_all_userdata__)        
        - [request_my_data](#__request_my_data__)        
        - [unsave_suggestion](#__unsave_suggestion__)    
    - [SubscriptionCog](#subscriptioncog)        
        - [new_topic](#__new_topic__)        
        - [remove_topic](#__remove_topic__)        
        - [topic_template](#__topic_template__)        
        - [unsubscribe](#__unsubscribe__)    
    - [TeamRosterCog](#teamrostercog)        
        - [delete_and_redo_team_roster](#__delete_and_redo_team_roster__)        
        - [force_update_team_roster](#__force_update_team_roster__)        
        - [initialize_team_roster](#__initialize_team_roster__)        
        - [team_roster_change_description](#__team_roster_change_description__)        
        - [team_roster_change_extra_role](#__team_roster_change_extra_role__)        
        - [team_roster_change_image](#__team_roster_change_image__)        
        - [team_roster_change_join_description](#__team_roster_change_join_description__)    
    - [TemplateCheckerCog](#templatecheckercog)        
        - [check_template](#__check_template__)    
    - [TranslateCog](#translatecog)        
        - [available_languages](#__available_languages__)        
        - [translate](#__translate__)  
  - [Special Permission Commands](#special-permission-commands)    
    - [Admin Lead Only](#admin-lead-only)  
  - [Misc](#misc)



---

## Info






### AdministrationCog

- __Config Name__
    administration

- __Description__
    Commands and methods that help in Administrate the Discord Server.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- OUTDATED

- NEEDS_REFRACTORING

- FEATURE_MISSING

- UNTESTED

- OPEN_TODOS
```
#### Commands:

##### __delete_msg__



- **aliases:** *delete+msg*, *delete.msg*, *delete-msg*, *deletemsg*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### AntistasiLogWatcherCog

- __Config Name__
    antistasi_log_watcher

- __Description__
    soon

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING

- UNTESTED

+ WORKING
```
#### Commands:

##### __get_newest_logs__

- **help:**

        Gets the newest log files from the Dev Drive.
        
        If the log file is bigger than current file size limit, it will provide it zipped.
        
        Tries to fuzzy match both server and sub-folder.
        
        Args:
            server (str): Name of the Server
            sub_folder (str): Name of the sub-folder e.g. Server, HC_0, HC_1,...
            amount (int, optional): The amount of log files to get. standard max is 5 . Defaults to 1.




- **aliases:** *get-newest-logs*, *getnewestlogs*, *get.newest.logs*, *get+newest+logs*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros get_newest_logs mainserver_1 server
    ```

<br>


##### __get_newest_mod_data__

- **help:**

        Gets the required mods for the Server.
        
        Provides the list as embed and Arma3 importable html file.
        
        Args:
            server (str): Name of the Antistasi Community Server to retrieve the mod list.




- **aliases:** *get-newest-mod-data*, *get.newest.mod.data*, *get+newest+mod+data*, *getnewestmoddata*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros get_newest_mod_data mainserver_1
    ```

<br>



---




### BotAdminCog

- __Config Name__
    bot_admin

- __Description__
    Commands and methods that are needed to Administrate the Bot itself.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING
```
#### Commands:

##### __add_to_blacklist__



- **aliases:** *add-to-blacklist*, *addtoblacklist*, *add.to.blacklist*, *add+to+blacklist*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __add_who_is_phrase__



- **aliases:** *add.who.is.phrase*, *add-who-is-phrase*, *addwhoisphrase*, *add+who+is+phrase*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __all_aliases__



- **aliases:** *all-aliases*, *allaliases*, *all+aliases*, *all.aliases*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __invocation_prefixes__



- **aliases:** *invocation.prefixes*, *invocation-prefixes*, *invocation+prefixes*, *invocationprefixes*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __life_check__



- **aliases:** *life.check*, *poke-with-stick*, *lifecheck*, *are-you-there*, *you_dead?*, *life-check*, *life+check*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __remove_from_blacklist__



- **aliases:** *remove-from-blacklist*, *removefromblacklist*, *remove+from+blacklist*, *remove.from.blacklist*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __self_announcement__



- **aliases:** *selfannouncement*, *self.announcement*, *self-announcement*, *self+announcement*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __send_log_file__

- **help:**

        Gets the log files of the bot and post it as a file to discord.
        
        You can choose to only get the newest or all logs.
        
        Args:
            which_logs (str, optional): [description]. Defaults to 'newest'. other options = 'all'




- **aliases:** *sendlogfile*, *send-log-file*, *send.log.file*, *send+log+file*


- **is hidden:** True

- **usage:**
    ```python
    @AntiPetros send_log_file all
    ```

<br>


##### __tell_uptime__



- **aliases:** *tell.uptime*, *tell+uptime*, *tell-uptime*, *telluptime*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __tell_version__



- **aliases:** *tell+version*, *tellversion*, *tell-version*, *tell.version*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### BotFeedbackCog

- __Config Name__
    bot_feedback

- __Description__
    WiP

- __Cog States__
```diff
- EMPTY

- DOCUMENTATION_MISSING

- CRASHING

- OUTDATED

- FEATURE_MISSING

- UNTESTED
```
#### Commands:


---




### CommunityServerInfoCog

- __Config Name__
    community_server_info

- __Description__
    soon

- __Cog States__
```diff
- EMPTY

- DOCUMENTATION_MISSING

- CRASHING

- OUTDATED

- FEATURE_MISSING

- UNTESTED
```
#### Commands:

##### __current_online_server__

- **help:**

        Shows all server of the Antistasi Community, that are currently online.
        
        Testserver_3 and Eventserver are excluded as they usually are password guarded.




- **aliases:** *current.online.server*, *currentonlineserver*, *current-online-server*, *current+online+server*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros current_online_server
    ```

<br>


##### __current_players__

- **help:**

        Show all players that are currently online on one of the Antistasi Community Server.
        
        Shows Player Name, Player Score and Time Played on that Server.
        
        Args:
            server (str): Name of the Server, case insensitive.




- **aliases:** *currentplayers*, *current.players*, *current-players*, *current+players*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros current_players mainserver_1
    ```

<br>


##### __exclude_from_server_status_notification__



- **aliases:** *exclude-from-server-status-notification*, *exclude.from.server.status.notification*, *excludefromserverstatusnotification*, *exclude+from+server+status+notification*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __undo_exclude_from_server_status_notification__



- **aliases:** *undoexcludefromserverstatusnotification*, *undo.exclude.from.server.status.notification*, *undo+exclude+from+server+status+notification*, *undo-exclude-from-server-status-notification*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>



---




### ConfigCog

- __Config Name__
    config

- __Description__
    Cog with commands to access and manipulate config files, also for changing command aliases.
    Almost all are only available in DM's
    
    commands are hidden from the help command.

- __Cog States__
```diff
- NEEDS_REFRACTORING

- FEATURE_MISSING

- OPEN_TODOS
```
#### Commands:

##### __add_alias__

- **help:**

        Adds an alias for a command.
        
        Alias has to be unique and not spaces.
        
        Args:
            command_name (str): name of the command
            alias (str): the new alias.




- **aliases:** *addalias*, *add.alias*, *add+alias*, *add-alias*


- **is hidden:** True

- **usage:**
    ```python
    @AntiPetros add_alias flip_coin flip_it
    ```

<br>


##### __change_setting_to__

- **help:**

        NOT IMPLEMENTED





- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __config_request__

- **help:**

        Returns a Config file as and attachment, with additional info in an embed.
        
        Args:
            config_name (str, optional): Name of the config, or 'all' for all configs. Defaults to 'all'.





- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __list_configs__

- **help:**

        NOT IMPLEMENTED




- **aliases:** *listconfigs*, *list+configs*, *list-configs*, *list.configs*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __overwrite_config_from_file__

- **help:**

        NOT IMPLEMENTED





- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __show_config_content__

- **help:**

        NOT IMPLEMENTED





- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __show_config_content_raw__

- **help:**

        NOT IMPLEMENTED





- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### FaqCog

- __Config Name__
    faq

- __Description__
    Creates Embed FAQ items.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING

- UNTESTED

+ WORKING
```
#### Commands:

##### __post_faq_by_number__

- **help:**

        Posts an FAQ as an embed on request.
        
        Either as an normal message or as an reply, if the invoking message was also an reply.
        
        Deletes invoking message
        
        Args:
            faq_numbers (commands.Greedy[int]): minimum one faq number to request, maximum as many as you want seperated by one space (i.e. 14 12 3)
            as_template (bool, optional): if the resulting faq item should be created via the templated items or from the direct parsed faqs.




- **aliases:** *postfaqbynumber*, *post+faq+by+number*, *post-faq-by-number*, *faq*, *post.faq.by.number*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>



---






### GiveAwayCog

- __Config Name__
    give_away

- __Description__
    Soon

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING
```
#### Commands:

##### __abort_give_away__

- **help:**

        NOT IMPLEMENTED




- **aliases:** *abort-give-away*, *abort.give.away*, *abort+give+away*, *abortgiveaway*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __create_giveaway__



- **aliases:** *giveaway*, *create.giveaway*, *creategiveaway*, *create+giveaway*, *create-giveaway*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __finish_give_away__

- **help:**

        NOT IMPLEMENTED




- **aliases:** *finish-give-away*, *finish+give+away*, *finish.give.away*, *finishgiveaway*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### ImageManipulatorCog

- __Config Name__
    image_manipulation

- __Description__
    Commands that manipulate or generate images.

- __Cog States__
```diff
- NEEDS_REFRACTORING

- FEATURE_MISSING

- OPEN_TODOS

+ WORKING
```
#### Commands:

##### __add_font__



- **aliases:** *add-font*, *add+font*, *add.font*, *addfont*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __add_stamp__

- **help:**

        Adds a new stamp image to the available stamps.
        
        This command needs to have the image as an attachment.




- **aliases:** *add+stamp*, *add.stamp*, *add-stamp*, *addstamp*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros add_stamp
    ```

<br>


##### __available_stamps__

- **help:**

        Posts all available stamps.




- **aliases:** *available-stamps*, *availablestamps*, *available.stamps*, *available+stamps*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros available_stamps
    ```

![](/art/finished/gifs/available_stamps_command.gif)

<br>


##### __list_fonts__



- **aliases:** *list-fonts*, *list.fonts*, *list+fonts*, *listfonts*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __member_avatar__

- **help:**

        Stamps the avatar of a Member with the Antistasi Crest.
        
        Returns the new stamped avatar as a .PNG image that the Member can save and replace his orginal avatar with.
        
        Example:
            @AntiPetros member_avatar





- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __stamp_image__

- **help:**

        Stamps an image with a small image from the available stamps.
        
        Usefull for watermarking images.
        
        Get all available stamps with '@AntiPetros available_stamps'




- **aliases:** *stamp.image*, *stamp-image*, *stamp+image*, *stampimage*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros stamp_image -si ASLOGO -fp bottom -sp right -so 0.5 -f 0.25
    ```

<br>


##### __text_to_image__



- **aliases:** *text+to+image*, *texttoimage*, *text.to.image*, *text-to-image*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>



---




### KlimBimCog

- __Config Name__
    klim_bim

- __Description__
    Collection of small commands that either don't fit anywhere else or are just for fun.

- __Cog States__
```diff
+ WORKING
```
#### Commands:

##### __choose_random__

- **help:**

        Selects random items from a semi-colon(`;`) seperated list. No limit on how many items the list can have, except for Discord character limit.
        
        Amount of item to select can be set by specifying a number before the list. Defaults to selecting only 1 item. Max amount is 25.
        
        Args:
        
            choices (str): input list as semi-colon seperated list.
            select_amount (Optional[int], optional): How many items to select. Defaults to 1.
        
        Example:
            `@AntiPetros 2 this is the first item; this is the second; this is the third`




- **aliases:** *choose+random*, *chooserandom*, *choose-random*, *choose.random*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __flip_coin__

- **help:**

        Simulates a coin flip and posts the result as an image of a Petros Dollar.




- **aliases:** *flip-coin*, *flipcoin*, *flip*, *flip.coin*, *coinflip*, *flip+coin*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros flip_coin
    ```

![](/art/finished/gifs/flip_coin_command.gif)

<br>


##### __make_figlet__

- **help:**

        Posts an ASCII Art version of the input text.
        
        **Warning, your invoking message gets deleted!**
        
        Args:
            text (str): text you want to see as ASCII Art.




- **aliases:** *make.figlet*, *makefiglet*, *make-figlet*, *make+figlet*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros make_figlet The text to figlet
    ```

![](/art/finished/gifs/make_figlet_command.gif)

<br>


##### __roll_dice__

- **help:**

        Roll Dice and get the result also as Image.
        
        All standard DnD Dice are available, d4, d6, d8, d10, d12, d20, d100.
        
        Args:
            dice_line (str): the dice you want to roll in the format `2d6`, first number is amount. Multiple different dice can be rolled, just seperate them by a space `2d6 4d20 1d4`.




- **aliases:** *roll.dice*, *roll-dice*, *rolldice*, *roll+dice*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __show_user_info__



- **aliases:** *show+user+info*, *show.user.info*, *showuserinfo*, *show-user-info*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __the_dragon__

- **help:**

        Posts and awesome ASCII Art Dragon!




- **aliases:** *thedragon*, *the.dragon*, *the+dragon*, *the-dragon*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros the_dragon
    ```

![](/art/finished/gifs/the_dragon_command.gif)

<br>


##### __urban_dictionary__

- **help:**

        Searches Urbandictionary for the search term and post the answer as embed
        
        Args:
        
            term (str): the search term
            entries (int, optional): How many UD entries for that term it should post, max is 5. Defaults to 1.




- **aliases:** *urbandictionary*, *urban+dictionary*, *urban-dictionary*, *urban.dictionary*


- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros urban_dictionary Petros 2
    ```

![](/art/finished/gifs/urban_dictionary_command.gif)

<br>



---




### PerformanceCog

- __Config Name__
    performance

- __Description__
    Collects Latency data and memory usage every 10min and posts every 24h a report of the last 24h as graphs.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- NEEDS_REFRACTORING

- FEATURE_MISSING

- OPEN_TODOS
```
#### Commands:

##### __get_command_stats__



- **aliases:** *get.command.stats*, *get+command+stats*, *getcommandstats*, *get-command-stats*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __initial_memory_use__



- **aliases:** *initial-memory-use*, *initial.memory.use*, *initial+memory+use*, *initialmemoryuse*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __report__

- **help:**

        Reports both current latency and memory usage as Graph.





- **is hidden:** True

- **usage:**
    ```python
    @AntiPetros report
    ```

<br>


##### __report_latency__



- **aliases:** *reportlatency*, *report-latency*, *report+latency*, *report.latency*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __report_memory__



- **aliases:** *report.memory*, *reportmemory*, *report-memory*, *report+memory*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### PurgeMessagesCog

- __Config Name__
    purge_messages

- __Description__
    Soon

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING
```
#### Commands:

##### __purge_antipetros__



- **aliases:** *purge-antipetros*, *purge+antipetros*, *purgeantipetros*, *purge.antipetros*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### SaveSuggestionCog

- __Config Name__
    save_suggestion

- __Description__
    Provides functionality for each Antistasi Team to save suggestions by reacting with emojis.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- NEEDS_REFRACTORING

- FEATURE_MISSING

- UNTESTED

- OPEN_TODOS

+ WORKING
```
#### Commands:

##### __auto_accept_suggestions__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __clear_all_suggestions__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __get_all_suggestions__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __mark_discussed__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __remove_all_userdata__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __request_my_data__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __unsave_suggestion__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### SubscriptionCog

- __Config Name__
    subscription

- __Description__
    Organizes Topic so they can be subscribed and mentioned selectively.

- __Cog States__
```diff
- DOCUMENTATION_MISSING

- FEATURE_MISSING
```
#### Commands:

##### __new_topic__



- **aliases:** *newtopic*, *new+topic*, *new-topic*, *new.topic*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __remove_topic__



- **aliases:** *remove+topic*, *remove-topic*, *remove.topic*, *removetopic*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __topic_template__



- **aliases:** *topic-template*, *topic.template*, *topictemplate*, *topic+template*


- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>


##### __unsubscribe__




- **is hidden:** True

- **usage:**
    ```python
    None
    ```

<br>



---




### TeamRosterCog

- __Config Name__
    team_roster

- __Description__
    WiP

- __Cog States__
```diff
- EMPTY

- DOCUMENTATION_MISSING

- CRASHING

- OUTDATED

- FEATURE_MISSING

- UNTESTED
```
#### Commands:

##### __delete_and_redo_team_roster__



- **aliases:** *delete-and-redo-team-roster*, *deleteandredoteamroster*, *delete+and+redo+team+roster*, *delete.and.redo.team.roster*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __force_update_team_roster__



- **aliases:** *forceupdateteamroster*, *force+update+team+roster*, *force.update.team.roster*, *force-update-team-roster*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __initialize_team_roster__



- **aliases:** *initializeteamroster*, *initialize-team-roster*, *initialize+team+roster*, *initialize.team.roster*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __team_roster_change_description__



- **aliases:** *team-roster-change-description*, *team+roster+change+description*, *teamrosterchangedescription*, *team.roster.change.description*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __team_roster_change_extra_role__



- **aliases:** *team+roster+change+extra+role*, *team.roster.change.extra.role*, *team-roster-change-extra-role*, *teamrosterchangeextrarole*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __team_roster_change_image__



- **aliases:** *team-roster-change-image*, *team+roster+change+image*, *team.roster.change.image*, *teamrosterchangeimage*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __team_roster_change_join_description__



- **aliases:** *teamrosterchangejoindescription*, *team.roster.change.join.description*, *team+roster+change+join+description*, *team-roster-change-join-description*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>



---




### TemplateCheckerCog

- __Config Name__
    template_checker

- __Description__
    soon

- __Cog States__
```diff
- EMPTY

- DOCUMENTATION_MISSING

- CRASHING

- OUTDATED

- FEATURE_MISSING

- UNTESTED
```
#### Commands:

##### __check_template__

- **help:**

        Checks all Classnames inside a provided template.
        
        Needs to have the tempalte as attachment to the invoking message.
        
        Returns the list of classnames it can't find in the config along with possible correction.
        
        Returns also a corrected version of the template file.
        
        Args:
            all_items_file (bool, optional): if it should also provide a file that lists all used classes. Defaults to True.
            case_insensitive (bool, optional): if it should check Case insentive. Defaults to False.




- **aliases:** *check-template*, *check.template*, *checktemplate*, *check+template*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>



---




### TranslateCog

- __Config Name__
    translate

- __Description__
    Collection of commands that help in translating text to different Languages.

- __Cog States__
```diff
+ WORKING
```
#### Commands:

##### __available_languages__



- **aliases:** *available.languages*, *availablelanguages*, *available+languages*, *available-languages*


- **is hidden:** False

- **usage:**
    ```python
    None
    ```

<br>


##### __translate__

- **help:**

        Translates text into multiple different languages.
        
        Tries to auto-guess input language.
        
        **Warning, your invoking message gets deleted!**
        
        Args:
            text_to_translate (str): the text to translate, quotes are optional
            to_language_id (Optional[LanguageConverter], optional): either can be the name of the language or an language code (iso639-1 language codes). Defaults to "english".





- **is hidden:** False

- **usage:**
    ```python
    @AntiPetros translate german This is the Sentence to translate
    ```

![](/art/finished/gifs/translate_command.gif)

<br>



---






## Special Permission Commands

### Admin Lead Only








- [delete_msg](#__delete_msg__)

















- [add_to_blacklist](#__add_to_blacklist__)





- [add_who_is_phrase](#__add_who_is_phrase__)











- [remove_from_blacklist](#__remove_from_blacklist__)











- [tell_version](#__tell_version__)

























- [add_alias](#__add_alias__)







































- [add_font](#__add_font__)







































- [get_command_stats](#__get_command_stats__)





- [initial_memory_use](#__initial_memory_use__)





- [report](#__report__)





- [report_latency](#__report_latency__)





- [report_memory](#__report_memory__)

















- [clear_all_suggestions](#__clear_all_suggestions__)






























































## Misc





