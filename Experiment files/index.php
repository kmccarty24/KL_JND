<!doctype html>
<html>
  <head>
    <title>Navon Figures task</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="jspsych-5.0/jspsych.js"></script>
	  <script src="jspsych-5.0/plugins/jspsych-text.js"></script>
	  <script src="jspsych-5.0/plugins/jspsych-single-stim.js"></script>
    <script src="jspsych-5.0/plugins/jspsych-survey-text.js"></script>
    <link href="jspsych-5.0/css/jspsych.css" rel="stylesheet" type="text/css"></link>
  </head>
  <body>
  </body>
  <script>

    function saveData(filename, filedata){
     $.ajax({
        type:'post',
        cache: false,
        url: 'save_data.php', // this is the path to the above PHP script
        data: {filename: filename, filedata: filedata}
     });
  }

    var subject_id = jsPsych.data.getURLVariable('id');
    
    var demographics = {
    type: 'survey-text',
    questions: ["Age", "Sex"]
  };

    jsPsych.data.addProperties({
    subject: subject_id
    });

    var welcome_block = {
    type: "text",
    text: "Welcome to the Navon Figures task. Press any key to begin."
  };
  
  /* define instructions block */
  var instructions_block = {
  type: "text",
  text: "<p>In this task, a large letter made of smaller letters will appear " +
        "either left or right of the screen.</p><p>If the large or small letter is E or H, " +
        "press the letter Y on the keyboard as fast as you can.</p>" +
        "<p>If these letters are not present, do not press " +
        "any key.</p>" +
        "<div class='left center-content'><img src='img/TeL.jpg'></img>" +
        "<p class='small'><strong>Press the   Y key</strong></p></div>" +
        "<div class='right center-content'><img src='img/LtR.jpg'></img>" +
        "<p class='small'><strong>Do not press a key</strong></p></div>" +
        "<p>Press any key to begin.</p>",
  timing_post_trial: 2000
  };



  var stimuli = [  
  {  
    stimulus: "img/EtL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/EtR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/EvL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/EvR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/HlL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/HlR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/HxL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/HxR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/LhL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/LhR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/LtL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/LtR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/LvL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/LvR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/TeL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/TeR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/TlL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/TlR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/TxL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/TxR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/VeL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/VeR.jpg",
    response: 'go'
  },
  {
    stimulus: "img/VlL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/VlR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/VxL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/VxR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/XhL.jpg",
    response: 'go'
  },
  {
    stimulus: "img/XhR.jpg",
    response: 'go'
},
    {
    stimulus: "img/XtL.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/XtR.jpg",
    response: 'no-go'
    },
  {
    stimulus: "img/XvL.jpg",
    response: 'no-go'
  },
  {
    stimulus: "img/XvR.jpg",
    response: 'no-go'
    }
  ];
  

    
  timeline = [];
  timeline.push(welcome_block);
  timeline.push(instructions_block);


  var random_order_stimuli = jsPsych.randomization.shuffle(stimuli, 2);

  for(var i = 0; i < random_order_stimuli.length; i++){
    
    var fixation_trial = { 
      type: "single-stim",
      stimulus: "img/0Fixation.jpg",
      response_ends_trial: false,
      timing_response: 500,
      timing_stim: 500,
      timing_post_trial: 0
      };

    timeline.push(fixation_trial);
  
    var navon_trial = {
      type: 'single-stim',
      stimulus: random_order_stimuli[i].stimulus,
      timing_stim: 150,
      timing_response: 150,
      timing_post_trial: 0
      };
    
    timeline.push(navon_trial);
    
    var mask_trial = { 
      type: "single-stim",
      stimulus: "img/1Mask.jpg",
      response: random_order_stimuli[i].response,
      data: {goNoGo: random_order_stimuli[i].response},
      choices: ['Y'],
      timing_response: 1500
      };

    timeline.push(mask_trial);
    };

  var debrief_block = {
    type: "text",
    text: "<p><strong>PARTICIPANT DEBRIEF</strong></p>" +
		"<p><strong>Name of researcher:</strong> Katie Linden</p>" +
		"<p><strong>Name of supervisor:</strong> Colin Hamilton</p>" +
		"<p><strong>Project title:</strong> Global and local processing in anorexia nervosa " +
		"with and without body image disturbances</p>" +
		"<p><strong>What was the purpose of the project?</strong></p>" +
		"<p>Previous research has suggested that people with anorexia nervosa are more " +
		"likely to notice the details of a task (local features) than the bigger picture " +
		"(global features). Some researchers theorise that this may relate to the experience " +
		"of body image disturbances: that people who focus on small areas of their body " +
		"are likely to perceive it as being out of proportion than people who can view their " +
		"body as a whole. Other researchers suggest this is part of a larger pattern in " +
		"cognitive processes that people with anorexia differ slightly from than people " +
		"without. The purpose of this research was to investigate whether people who have " +
        "anorexia without body image disturbances also experience this local bias in processing.</p>" +
		"<p><strong>How will I find out about the results?</strong></p>" +
		"<p>If you would like to know the results of this study, please contact Katie Linden " +
		"(katie.linden@northumbria.ac.uk). You will then be given a summary once the " +
		"results have been analysed.</p>" +
		"<p><strong>Have I been deceived in any way during the project?</strong></p>" +
		"<p>You were given accurate information about the nature of this study and the tasks " +
		"you were to complete prior to taking part. However, you were not informed that this " +
		"study was looking specifically at potential biases in perception where individuals " +
		"pay attention to small details in an image. This knowledge may have made you more " +
		"likely to focus on the details of the cognitive tasks. If you are uncomfortable with " +
		"this and would like to withdraw from this study, please see the following question " +
		"for information</p>" +
		"<p><strong>If I change my mind and wish to withdraw the information I have provided, " +
		"how do I do this?</strong></p>" +
		"<p>You can withdraw from this study at any time within the next month. If you would " +
		"like to withdraw from the study, please email Katie Linden (katie.linden@northumbria.ac.uk) " +
		"quoting the code word that you provided us with at the beginning of the study. We will " +
		"then destroy the information that you have given to us. If you email to be withdrawn " +
		"from the study after 1 month it may not be possible to remove you from the study, " +
		"as the data may already have been analysed.</p>" +
		"<p><strong>Who can I contact if I am concerned about problems with food or weight?</strong></p>" +
		"<p>Your GP can give you information about local services supporting people with eating " +
		"disorders. Beat (http://www.b-eat.co.uk) are a UK charity who run a helpline for " +
		"people who are concerned about eating disorders, contact number 0345 634 1414. Men Get " +
		"Men Get Eating Disorders Too are a national organisation based in Brighton, for men who " +
		"have issues with eating or body image (http://mengetedstoo.co.uk). In Newcastle and " +
		"the North East, NIWE Eating Distress Service provide information, support and signposting " +
		"to people affected by eating distress (http://www.niwe.org.uk).</p>" +
		"<p>If you have any concerns or worries concerning this research or if you wish to register " +
		"a complaint, please direct it to the Department of Psychology Ethics Chair (Postgraduate) " +
		"at the address below, or by email: andriy.myachykov@northumbria.ac.uk The data collected " +
		"in this study will be used for a Postgraduate Psychology Thesis. It may also be " +
		"published in scientific journals or presented at conferences. Information and data " +
		"gathered during this research study will only be available to the research team named " +
		"team named above, and the Postgraduate Ethics Chair (Andriy Myachykov). Should the research " +
		"be presented or published in any form, all data will be anonymous (i.e. your personal " +
		"information or data will not be identifiable). All information and data gathered " +
		"during this research will be stored in line with the Data Protection Act and will " +
		"be destroyed 6 months following the conclusion of the study. If the research is " +
		"published in a scientific journal it may be kept for longer before being destroyed. During " +
		"that time the data may be used by members of the research team only for purposes " +
		"appropriate to the research question, but at no point will your personal information or " +
		"data be revealed. Insurance companies and employers will not be given any individual's " +
		"information, samples, or test results, and nor will we allow access to the police, " +
		"security services, social services, relatives or lawyers, unless forced to do so by " +
		"the courts. This study and its protocol have received full ethical approval from " +
		"the Department of Psychology Ethics Committee (Postgraduate) in accordance with the " +
		"School of Health and Life Sciences Ethics Committee. If you require confirmation " +
		"of this please contact the Chair of this Committee on the details below, stating the title of the research " +
		"project and the name of the researcher: </p>" +
		"<p>Dr Andriy Myachykov<br>" +
		"Chair of Department of Psychology Ethics Committee (Postgraduate)<br>" +
		"Northumbria University<br>" +
		"Newcastle upon Tyne<br>" +
		"NE1 8ST<br>" +
		"UK</p>",
  };

  timeline.push(debrief_block);

  console.log(timeline);
  /* start the experiment */
  jsPsych.init({
    timeline: timeline,
    on_finish: function(data){saveData(subject_id + '.csv', jsPsych.data.dataAsCSV())}
    });

</script>
</html>