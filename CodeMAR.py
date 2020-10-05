---
API: 2.1
OpenSesame: 3.3.4a13
Platform: posix
---
set width 1024
set uniform_coordinates yes
set title "SlimStampen example"
set subject_parity even
set subject_nr 0
set start experiment
set sound_sample_size -16
set sound_freq 48000
set sound_channels 2
set sound_buf_size 1024
set sampler_backend psycho
set round_decimals 2
set mouse_backend psycho
set keyboard_backend psycho
set height 768
set fullscreen no
set form_clicks no
set foreground white
set font_underline no
set font_size 20
set font_italic no
set font_family mono
set font_bold no
set experiment_path "/Users/annikaschnabel/Documents/UserModels/user-models-2020-master"
set disable_garbage_collection yes
set description "The main experiment item"
set coordinates uniform
set compensation 0
set color_backend psycho
set clock_backend psycho
set canvas_backend psycho
set background black

define inline_script User
	set description "Führt Python Code aus"
	___run__
	my_canvas = Canvas()
	my_canvas['Instruction'] = Text("Please enter a user name (no upper case letters):", y = -20, font_size = 25, color = "white")
	my_canvas.prepare()
	my_canvas.show()
	# Listen for keyboard input and show keypresses on screen as they occur
	my_keyboard = Keyboard()
	my_keyboard.timeout = 3000
	keyboard_response = ""
	erased_answer = False

	# Keep listening for key presses until the user presses Enter
	while True:
	    key, time = my_keyboard.get_key()

	    if key == "return":
	        break

	    if key == "backspace":
	        keyboard_response = keyboard_response[:-1]
	        # If the answer is completely erased, the RT is no longer informative
	        if keyboard_response == "":
	            erased_answer = True

	    elif key == "space":
	        keyboard_response += " "

	    elif not key == None:

	        keyboard_response += my_keyboard.to_chr(key)

	    # Update what's on screen'
	    my_canvas.clear()
	    my_canvas['Instruction'] = Text("Please enter a user name (no upper case letters):", y = -20, font_size = 25, color = "white")
	    my_canvas.text(keyboard_response, y = 30)
	    my_canvas.prepare()
	    my_canvas.show()
	#print(F'user name: {keyboard_response}')
	exp.set('user', keyboard_response)
	#useranswer = self.get('user')
	#print(F'username: {useranswer}')
	__end__
	set _prepare ""

define sequence experiment
	set flush_keyboard yes
	set description "Runs a number of items in sequence"
	run instructions always
	run slimstampen_setup always
	run scoring always
	run User always
	run learning_session_setup always
	run while_there_is_time_left always
	run feedback_text always
	run new_feedback always
	run test_instructions always
	run save_data always
	run new_inline_script always
	run new_loop always
	run test_feedback always
	run new_feedback_1 always

define inline_script feedback_text
	set description "Führt Python Code aus"
	___run__
	acc = 100.*self.get('total_correct')/self.get('total_responses')

	exp.set('accuracy', acc)
	exp.set('acc', acc)

	if self.get('acc') > 90:
		exp.set('feedback_msg', 'Excellent, well done!')
	elif self.get('acc') > 75:
		exp.set('feedback_msg', 'Pretty good!')
	else:
		exp.set('feedback_msg', 'Come on, you can do better!')

	data = {'User':[self.get('user')],'Score':[self.get('total_correct')], 'Possible Score':[self.get('total_responses')],
		'Accuracy':[self.get('accuracy')]}

	# Create DataFrame
	df = pd.DataFrame(data)
	#df.to_csv("your_name.csv", encoding = 'utf-8')

	def export_output(dat, path = None):
	        # type: (str) -> DataFrame

	        if path is not None:
	            dat.to_csv(path, encoding="UTF-8")
	            return(dat)

	        return(dat.to_csv())
	ex = export_output(df)
	log.write(ex)
	__end__
	set _prepare ""

define sketchpad instructions
	set duration keypress
	set description "Displays stimuli"
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=18 html=yes show_if=always text="Hello, Welcome to Melting Active Retrieval. For each english word enter the translation. If you do not know the answer hints will be given to you after 3 seconds. If you do not know the answer just give a random letter and press enter. <br><br> Press enter to continue." x=0 y=96 z_index=0
	draw image center=1 file="result-3236280__480.jpg" scale=0.75 show_if=always x=0 y=-160 z_index=0

define inline_script learning_session_setup
	set description "Executes Python code"
	___run__
	# Start the clock
	var.session_start_time = clock.time()

	# Session will run until time_up == True
	var.time_up = False

	# Keep track of trial number
	var.trial_num = 1

	# Settings
	var.session_duration = 10000
	var.feedback_duration = 800
	var.inter_trial_interval = 200

	exp.set('total_responses', 0)
	exp.set('total_correct', 0)
	exp.set('accuracy', 'NA')
	exp.set('acc', 'NA')
	__end__
	set _prepare ""

define feedback new_feedback
	set reset_variables yes
	set duration keypress
	set description "Gibt Versuchspersonen Feedback"
	draw image center=1 file="fax-1889009__480.jpg" scale=0.5 show_if=always x=0 y=-208 z_index=1
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=18 html=yes show_if=always text="[feedback_msg] You have a score of [total_correct] from [total_responses] possible points. That corresponds to an accuracy of [accuracy]%." x=0 y=0 z_index=0

define feedback new_feedback_1
	set reset_variables yes
	set duration keypress
	set description "Gibt Versuchspersonen Feedback"
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=20 html=yes show_if=always text="[feedback_test] You have [correct_test] from [responses_test] possible answers correct. That corresponds to an accuracy of [accuracy_test]%." x=0.0 y=0.0 z_index=0

define inline_script new_inline_script
	set description "Führt Python Code aus"
	___run__
	# Settings
	# Keep track of trial number
	var.trial_num = 1
	var.session_start_test = clock.time()
	var.voc = 'english'
	var.ans = 'french'
	var.inter_trial_test = 200
	exp.set('score_test', 100)
	exp.set('correct_test', 0)
	exp.set('responses_test', 0)

	var.session_test = 10000
	var.feedback_test = 800
	var.inter_trial_test = 200
	__end__
	set _prepare ""

define loop new_loop
	set source_file ""
	set source table
	set repeat 1
	set order sequential
	set description "Führt wiederholt ein anderes Item aus"
	set cycles 4
	set continuous no
	set break_if_on_first yes
	set break_if never
	setcycle 0 english hello
	setcycle 0 french bonjour
	setcycle 1 english dog
	setcycle 1 french chien
	setcycle 2 english cat
	setcycle 2 french chat
	setcycle 3 english car
	setcycle 3 french voiture
	run new_sequence

define sequence new_sequence
	set flush_keyboard yes
	set description "Führt mehrere Items nacheinander aus"
	run present_trial_testing always

define sketchpad new_sketchpad
	set duration keypress
	set description "Präsentiert Stimuli"
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=20 html=yes show_if=always text="[feedback_test] You have [correct_test] from [responses_test] correct. That equals an accuracy of [accuracy_test]." x=-5632 y=-256 z_index=0

define sketchpad new_sketchpad_1
	set duration keypress
	set description "Präsentiert Stimuli"

define inline_script present_trial
	set description "Executes Python code"
	___run__
	trial_start_time = clock.time()

	# Get next fact from the model
	next_fact, new = m.get_next_fact(current_time = trial_start_time)
	prompt = next_fact.question
	answer = next_fact.answer

	# Show prompt
	my_canvas = Canvas()
	exp.set('score', 100)
	#my_canvas['my_score'] = Text(score,x = -160, y = -30, font_size = 30, color = "yellow")
	#my_canvas['my_correct'] = Text(self.get("total_correct"),x = 160, y = -30, font_size = 30, color = "purple")
	my_canvas['name_score'] = Text("Score",x = -160, y = -70, font_size = 30, color = "yellow")
	if not new:
	    my_canvas['start_score'] = Text(exp.get('score'),x = -160, y = -30, font_size = 20, color = "yellow")
	else:
	    my_canvas['start_score'] = Text(" ",x = -160, y = -30, font_size = 20, color = "yellow")
	my_canvas['name_correct'] = Text("Total", x = 160, y = -70, font_size = 30, color = "purple")
	my_canvas['start_correct'] = Text(self.get("total_correct"), x = 160, y = -30, font_size = 20, color = "purple")
	my_canvas.text(prompt, font_size = 30)
	if new:
	    my_canvas.text(answer, y = 50, font_size = 20)
	my_canvas.prepare()
	my_canvas.show()

	# Listen for keyboard input and show keypresses on screen as they occur
	my_keyboard = Keyboard()
	my_keyboard.timeout = 3000
	keyboard_response = ""
	erased_answer = False
	rt = float("inf")
	cnt = 0
	#exp.set('cnt',-1)
	#exp.set('hint',0)
	hint = 0
	hint_stop = 0
	# Keep listening for key presses until the user presses Enter
	while True:
	    key, time = my_keyboard.get_key()

	    # Give hints if time limit is over
	    if keyboard_response == "" and not new:
	        #print(u'Give a hint!')
	        #exp.set('hint',1)
	        hint = 1
	        print(F'all set {hint}')
	        #exp.set('cnt', self.get('cnt')+1)
	        if not hint_stop:
	            cnt += 1
	            exp.set('score', self.get('score')-10)
	        print(F"counter incremented to: {cnt}")

	    else:
	        #exp.set('hint',0)
	        hint = 0
	        print(F'Dont give a hint {hint}')

	    if cnt-1 > len(answer)/2:
	        hint_stop = 1

	    # The first keypress determines the response time
	    if keyboard_response == "" and not erased_answer:
	        rt = clock.time() - trial_start_time

	    #if keyboard_response == NoneType:
	    #print(u'Keyboard responce empty')

	    if key == "return":
	        break

	    if key == "backspace":
	        keyboard_response = keyboard_response[:-1]
	        # If the answer is completely erased, the RT is no longer informative
	        if keyboard_response == "":
	            erased_answer = True
	            rt = float("inf")
	            hint_stop = 0

	    elif key == "space":
	        keyboard_response += " "

	    elif not key == None:

	        keyboard_response += my_keyboard.to_chr(key)

	    # Update what's on screen'
	    my_canvas.clear()
	    my_canvas.text(prompt, font_size = 30)
	    my_canvas['name_score'] = Text("Score",x = -160, y = -70, font_size = 30, color = "yellow")
	    if not new:
	        my_canvas['my_score'] = Text(exp.get('score'),x = -160, y = -30, font_size = 20, color = "yellow")
	    else:
	        my_canvas['my_score'] = Text(" ",x = -160, y = -30, font_size = 20, color = "yellow")
	    my_canvas['name_correct'] = Text("Total", x = 160, y = -70, font_size = 30, color = "purple")
	    my_canvas['my_correct'] = Text(self.get("total_correct"), x = 160, y = -30, font_size = 20, color = "purple")
	    #my_canvas.text(score,x = -160, y = -30, font_size = 30, color = "yellow")
	    #my_canvas.text(self.get("total_correct"),x = 160, y = -30, font_size = 30, color = "purple")
	    if new:
	        my_canvas.text(answer, y = 50, font_size = 20)
	    my_canvas.text(keyboard_response, y = 100)
	    if hint:
	        #self.get('hint'):
	        # #clue = str(answer[: self.get('cnt')]) + str("_" * (len(answer)-self.get('cnt')))
	        clue = answer[: cnt-1] + "- " * (len(answer)-(cnt-1))
	        print(F'current clue: {clue}')
	        my_canvas.text(clue, y=-120, font_size = 30)
	    my_canvas.prepare()
	    my_canvas.show()

	# Check if the response is correct
	correct = keyboard_response == answer

	# Log response
	response = Response(next_fact, trial_start_time, rt, correct)
	m.register_response(response)

	# Set score
	if not new:
	    if not correct:
	        exp.set('score', 0)
	    exp.set('total_responses', self.get('total_responses')+100)
	    exp.set('total_correct', self.get('total_correct')+self.get('score'))
	else:
		exp.set('score', " ")

	# Show feedback
	feedback_color = "green" if correct else "red"
	my_canvas.text(keyboard_response, y = 100, color = feedback_color)
	if not new:
	    my_canvas['my_score'].color = 'black'
	if correct:
	    my_canvas.text(self.get('score'),x = -160, y = -30, font_size = 20, color = "blue")
	else:
	    my_canvas.text(self.get('score'),x = -160, y = -30, font_size = 20, color = "red")
	    my_canvas.text(answer, y = 150)
	my_canvas['my_correct'].color = 'black'
	my_canvas.text(self.get("total_correct"),x = 160, y = -30, font_size = 20, color = "purple")
	my_canvas.prepare()
	my_canvas.show()
	clock.sleep(var.feedback_duration)

	# Clear the screen between trials
	my_canvas.clear()
	my_canvas.prepare()
	my_canvas.show()
	clock.sleep(var.inter_trial_interval)

	# Check if time is up
	if clock.time() - var.session_start_time >= var.session_duration:
	    var.time_up = True

	# Increment trial number
	var.trial_num += 1
	__end__
	set _prepare ""

define inline_script present_trial_testing
	set description "Executes Python code"
	___run__
	trial_start_test = clock.time()

	# Get next fact from the model
	voc = var.english
	ans = var.french

	# Show prompt
	my_canvas = Canvas()
	my_canvas.text(voc, font_size = 30)
	my_canvas.prepare()
	my_canvas.show()

	# Listen for keyboard input and show keypresses on screen as they occur
	my_keyboard = Keyboard()
	my_keyboard.timeout = 3000
	keyboard_response = ""
	erased_answer = False
	rt = float("inf")

	# Keep listening for key presses until the user presses Enter
	while True:
	    key, time = my_keyboard.get_key()

	    # The first keypress determines the response time
	    if keyboard_response == "" and not erased_answer:
	        rt = clock.time() - trial_start_test

	    #if keyboard_response == NoneType:
	    #print(u'Keyboard responce empty')

	    if key == "return":
	        break

	    if key == "backspace":
	        keyboard_response = keyboard_response[:-1]
	        # If the answer is completely erased, the RT is no longer informative
	        if keyboard_response == "":
	            erased_answer = True
	            rt = float("inf")

	    elif key == "space":
	        keyboard_response += " "

	    elif not key == None:

	        keyboard_response += my_keyboard.to_chr(key)

	    # Update what's on screen'
	    my_canvas.clear()
	    my_canvas.text(voc, font_size = 30)

	    my_canvas.text(keyboard_response, y = 100)

	    my_canvas.prepare()
	    my_canvas.show()

	# Check if the response is correct
	correct = keyboard_response == ans

	# Set score
	exp.set('responses_test', self.get('responses_test')+1)
	if correct:
	    exp.set('correct_test', self.get('correct_test')+1)

	# Clear the screen between trials
	my_canvas.clear()
	my_canvas.prepare()
	my_canvas.show()
	clock.sleep(var.inter_trial_test)

	# Check if time is up
	if clock.time() - var.session_start_test >= var.session_test:
	    var.time_up = True

	# Increment trial number
	var.trial_num += 1
	__end__
	set _prepare ""

define inline_script save_data
	set description "Executes Python code"
	___run__
	# Write the SlimStampen data to the OpenSesame log file
	dat = m.export_data()
	log.write(dat)
	__end__
	set _prepare ""

define sketchpad scoring
	set duration keypress
	set description "Präsentiert Stimuli"
	draw rect color=orange fill=orange h=192 penwidth=5 show_if=always w=448 x=-224 y=-224 z_index=1
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=18 html=yes show_if=always text="<span style='font-size:32px;'>Scoring</span> <br><br />correct answer = 100 points<br />each hint = -10 points<br />wrong answer = 0 point<br />new word (translation given) = 0 points<br /><br> <br><br />After the learning session your score will be displayed and after the experiment a ranking of the highscores from all participants will be send to you.<br /><br />Press enter to start the learning session" x=0 y=-64 z_index=0

define inline_script slimstampen_setup
	set description "Executes Python code"
	___run__
	m = SpacingModel()

	# Add some study facts to the model (you could also read them from a CSV file)
	facts = [Fact(1, "hello", "bonjour"),
			Fact(2, "dog", "chien"),
			Fact(3, "cat", "chat"),
			Fact(4, "computer", "ordinateur"),
			Fact(5, "house", "maison"),
			Fact(6, "car", "voiture"),
			Fact(7, "fish", "poisson"),
			Fact(8, "bottle", "bouteille")]

	for fact in facts:
		m.add_fact(fact)
	__end__
	___prepare__
	from __future__ import division
	import math
	import pandas as pd
	from collections import namedtuple

	Fact = namedtuple("Fact", "fact_id, question, answer")
	Response = namedtuple("Response", "fact, start_time, rt, correct")
	Encounter = namedtuple("Encounter", "activation, time, reaction_time, decay")


	class SpacingModel(object):

	    # Model constants
	    LOOKAHEAD_TIME = 15000
	    FORGET_THRESHOLD = -0.8
	    DEFAULT_ALPHA = 0.3
	    C = 0.25
	    F = 1.0

	    def __init__(self):
	        self.facts = []
	        self.responses = []

	    def add_fact(self, fact):
	        # type: (Fact) -> None
	        """
	        Add a fact to the list of study items.
	        """
	        # Ensure that a fact with this ID does not exist already
	        if next((f for f in self.facts if f.fact_id == fact.fact_id), None):
	            raise RuntimeError(
	                "Error while adding fact: There is already a fact with the same ID: {}. Each fact must have a unique ID".format(fact.fact_id))

	        self.facts.append(fact)


	    def register_response(self, response):
	        # type: (Response) -> None
	        """
	        Register a response.
	        """
	        # Prevent duplicate responses
	        if next((r for r in self.responses if r.start_time == response.start_time), None):
	            raise RuntimeError(
	                "Error while registering response: A response has already been logged at this start_time: {}. Each response must occur at a unique start_time.".format(response.start_time))

	        self.responses.append(response)


	    def get_next_fact(self, current_time):
	        # type: (int) -> (Fact, bool)
	        """
	        Returns a tuple containing the fact that needs to be repeated most urgently and a boolean indicating whether this fact is new (True) or has been presented before (False).
	        If none of the previously studied facts needs to be repeated right now, return a new fact instead.
	        """
	        # Calculate all fact activations in the near future
	        fact_activations = [(f, self.calculate_activation(current_time + self.LOOKAHEAD_TIME, f)) for f in self.facts]

	        seen_facts = [(f, a) for (f, a) in fact_activations if a > -float("inf")]
	        not_seen_facts = [(f, a) for (f, a) in fact_activations if a == -float("inf")]

	        # Prevent an immediate repetition of the same fact
	        if len(seen_facts) > 2:
	            last_response = self.responses[-1]
	            seen_facts = [(f, a) for (f, a) in seen_facts if f.fact_id != last_response.fact.fact_id]

	        # Reinforce the weakest fact with an activation below the threshold
	        seen_facts_below_threshold = [(f, a) for (f, a) in seen_facts if a < self.FORGET_THRESHOLD]
	        if len(not_seen_facts) == 0 or len(seen_facts_below_threshold) > 0:
	            weakest_fact = min(seen_facts, key = lambda t: t[1])
	            return((weakest_fact[0], False))

	        # If none of the previously seen facts has an activation below the threshold, return a new fact
	        return((not_seen_facts[0][0], True))


	    def get_rate_of_forgetting(self, time, fact):
	        # type: (int, Fact) -> float
	        """
	        Return the estimated rate of forgetting of the fact at the specified time
	        """
	        encounters = []

	        responses_for_fact = [r for r in self.responses if r.fact.fact_id == fact.fact_id and r.start_time < time]
	        alpha = self.DEFAULT_ALPHA

	        # Calculate the activation by running through the sequence of previous responses
	        for response in responses_for_fact:
	            activation = self.calculate_activation_from_encounters(encounters, response.start_time)
	            encounters.append(Encounter(activation, response.start_time, self.normalise_reaction_time(response), self.DEFAULT_ALPHA))
	            alpha = self.estimate_alpha(encounters, activation, response, alpha)

	            # Update decay estimates of previous encounters
	            encounters = [encounter._replace(decay = self.calculate_decay(encounter.activation, alpha)) for encounter in encounters]

	        return(alpha)


	    def calculate_activation(self, time, fact):
	        # type: (int, Fact) -> float
	        """
	        Calculate the activation of a fact at the given time.
	        """

	        encounters = []

	        responses_for_fact = [r for r in self.responses if r.fact.fact_id == fact.fact_id and r.start_time < time]
	        alpha = self.DEFAULT_ALPHA

	        # Calculate the activation by running through the sequence of previous responses
	        for response in responses_for_fact:
	            activation = self.calculate_activation_from_encounters(encounters, response.start_time)
	            encounters.append(Encounter(activation, response.start_time, self.normalise_reaction_time(response), self.DEFAULT_ALPHA))
	            alpha = self.estimate_alpha(encounters, activation, response, alpha)

	            # Update decay estimates of previous encounters
	            encounters = [encounter._replace(decay = self.calculate_decay(encounter.activation, alpha)) for encounter in encounters]

	        return(self.calculate_activation_from_encounters(encounters, time))


	    def calculate_decay(self, activation, alpha):
	        # type: (float, float) -> float
	        """
	        Calculate activation-dependent decay
	        """
	        return self.C * math.exp(activation) + alpha


	    def estimate_alpha(self, encounters, activation, response, previous_alpha):
	        # type: ([Encounter], float, Response, float) -> float
	        """
	        Estimate the rate of forgetting parameter (alpha) for an item.
	        """
	        if len(encounters) < 3:
	            return(self.DEFAULT_ALPHA)

	        a_fit = previous_alpha
	        reading_time = self.get_reading_time(response.fact.question)
	        estimated_rt = self.estimate_reaction_time_from_activation(activation, reading_time)
	        est_diff = estimated_rt - self.normalise_reaction_time(response)

	        if est_diff < 0:
	            # Estimated RT was too short (estimated activation too high), so actual decay was larger
	            a0 = a_fit
	            a1 = a_fit + 0.05

	        else:
	            # Estimated RT was too long (estimated activation too low), so actual decay was smaller
	            a0 = a_fit - 0.05
	            a1 = a_fit

	        # Binary search between previous fit and proposed alpha
	        for _ in range(6):
	            # Adjust all decays to use the new alpha
	            a0_diff = a0 - a_fit
	            a1_diff = a1 - a_fit
	            d_a0 = [e._replace(decay = e.decay + a0_diff) for e in encounters]
	            d_a1 = [e._replace(decay = e.decay + a1_diff) for e in encounters]

	            # Calculate the reaction times from activation and compare against observed RTs
	            encounter_window = encounters[max(1, len(encounters) - 5):]
	            total_a0_error = self.calculate_predicted_reaction_time_error(encounter_window, d_a0, reading_time)
	            total_a1_error = self.calculate_predicted_reaction_time_error(encounter_window, d_a1, reading_time)

	            # Adjust the search area based on the lowest total error
	            ac = (a0 + a1) / 2
	            if total_a0_error < total_a1_error:
	                a1 = ac
	            else:
	                a0 = ac

	        # The new alpha estimate is the average value in the remaining bracket
	        return((a0 + a1) / 2)


	    def calculate_activation_from_encounters(self, encounters, current_time):
	        # type: ([Encounter], int) -> float
	        included_encounters = [e for e in encounters if e.time < current_time]

	        if len(included_encounters) == 0:
	            return(-float("inf"))

	        return(math.log(sum([math.pow((current_time - e.time) / 1000, -e.decay) for e in included_encounters])))


	    def calculate_predicted_reaction_time_error(self, test_set, decay_adjusted_encounters, reading_time):
	        # type: ([Encounter], [Encounter], Fact) -> float
	        """
	        Calculate the summed absolute difference between observed response times and those predicted based on a decay adjustment.
	        """
	        activations = [self.calculate_activation_from_encounters(decay_adjusted_encounters, e.time - 100) for e in test_set]
	        rt = [self.estimate_reaction_time_from_activation(a, reading_time) for a in activations]
	        rt_errors = [abs(e.reaction_time - rt) for (e, rt) in zip(test_set, rt)]
	        return(sum(rt_errors))


	    def estimate_reaction_time_from_activation(self, activation, reading_time):
	        # type: (float, int) -> float
	        """
	        Calculate an estimated reaction time given a fact's activation and the expected reading time
	        """
	        return((self.F * math.exp(-activation) + (reading_time / 1000)) * 1000)


	    def get_max_reaction_time_for_fact(self, fact):
	        # type: (Fact) -> float
	        """
	        Return the highest response time we can reasonably expect for a given fact
	        """
	        reading_time = self.get_reading_time(fact.question)
	        max_rt = 1.5 * self.estimate_reaction_time_from_activation(self.FORGET_THRESHOLD, reading_time)
	        return(max_rt)


	    def get_reading_time(self, text):
	        # type: (str) -> float
	        """
	        Return expected reading time in milliseconds for a given string
	        """
	        word_count = len(text.split())

	        if word_count > 1:
	            character_count = len(text)
	            return(max((-157.9 + character_count * 19.5), 300))

	        return(300)


	    def normalise_reaction_time(self, response):
	        # type: (Response) -> float
	        """
	        Cut off extremely long responses to keep the reaction time within reasonable bounds
	        """
	        rt = response.rt if response.correct else 60000
	        max_rt = self.get_max_reaction_time_for_fact(response.fact)
	        return(min(rt, max_rt))


	    def export_data(self, path = None):
	        # type: (str) -> DataFrame
	        """
	        Save the response data to the specified csv file, and return a copy of the pandas DataFrame.
	        If no path is specified, return a CSV-formatted copy of the data instead.
	        """

	        def calc_rof(row):
	            return(self.get_rate_of_forgetting(row["start_time"] + 1, row["fact"]))

	        dat_resp = pd.DataFrame(self.responses)
	        dat_facts = pd.DataFrame([r.fact for r in self.responses])
	        dat = pd.concat([dat_resp, dat_facts], axis = 1)

	        # Add column for rate of forgetting estimate after each observation
	        dat["alpha"] = dat.apply(calc_rof, axis = 1)
	        dat.drop(columns = "fact", inplace = True)

	        # Add trial number column
	        dat.index.name = "trial"
	        dat.index = dat.index + 1

	        # Save to CSV file if a path was specified, otherwise return the CSV-formatted output
	        if path is not None:
	            dat.to_csv(path, encoding="UTF-8")
	            return(dat)

	        return(dat.to_csv())
	__end__

define inline_script test_feedback
	set description "Führt Python Code aus"
	___run__
	acc_test = 100.*self.get('correct_test')/self.get('responses_test')

	exp.set('accuracy_test', acc_test)
	exp.set('acc_test', acc_test)

	if self.get('acc_test') > 90:
		exp.set('feedback_test', 'Excellent, well done!')
	elif self.get('acc_test') > 75:
		exp.set('feedback_test', 'Pretty good!')
	else:
		exp.set('feedback_test', 'Come on, you can do better!')

	data_test = {'Score':[self.get('correct_test')], 'Possible Score':[self.get('responses_test')],
		'Accuracy':[self.get('accuracy_test')]}

	# Create DataFrame
	df_test = pd.DataFrame(data_test)
	#df.to_csv("your_name.csv", encoding = 'utf-8')

	def export_output(dat, path = None):
	        # type: (str) -> DataFrame

	        if path is not None:
	            dat.to_csv(path, encoding="UTF-8")
	            return(dat)

	        return(dat.to_csv())
	ex_test = export_output(df_test)
	log.write(ex_test)
	__end__
	set _prepare ""

define sketchpad test_instructions
	set duration keypress
	set description "Präsentiert Stimuli"
	draw textline center=1 color=white font_bold=no font_family=mono font_italic=no font_size=20 html=yes show_if=always text="In the following section your learning progress will be tested. Please type the corresponding translation." x=0 y=0 z_index=0

define sequence trial_sequence
	set flush_keyboard yes
	set description "Runs a number of items in sequence"
	run present_trial always

define loop while_there_is_time_left
	set source table
	set repeat 1000
	set order random
	set description "Repeatedly runs another item"
	set cycles 1
	set continuous no
	set break_if_on_first yes
	set break_if "[time_up] = yes"
	setcycle 0 ignore_this_variable 1
	run trial_sequence
