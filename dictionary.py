TEXTS = {
    'languages' : {
        'es': {
            'languages_options': {
                'welcome': '🇪🇸 ¡Hola! ¿En qué idioma prefieres continuar?',
                'button_text': '🇪🇸 Español',
                'option': 'es',
                'language_selected': '🇪🇸 Has seleccionado el idioma en Español.'
            },
            'game_options': {
                'titles': {
                    'mode_game': '👾Seleccione un modo de juego.👾',
                    'game_selected': 'Has seleccionado el modo de ',
                    'final_answer' : '🏁La fecha y hora que elegiste es: ',
                    'release_date' : '🚀La fecha y hora del lanzamiento fue:',
                    'correct' : '🚀🥳¡El cohete despegó!🥳🚀',
                    'false' : '🚀😓¡El cohete no había despago!😓🚀',
                    'limit' : '😨Llegaste al límite de cuadros de este vídeo.😨',
                    'goodbye' : 'Gracias por jugar, nos conectamos en una proxima.\n\n/start',
                },
                'one': {
                    'description': 'Juego 1️⃣.\nPregunta: ¿Ya despego el cohete?\nOpciones:\n🔹Sí: proporciona la fecha del lanzamiento.\n🔹No: sigue jugando.',
                    'option':'Juego 1️⃣',
                    'option_selected': 'one',
                    'options': {'question': '¿Ya despego el cohete?', 'answer_text': {'one':'🚀 Sí, ya despego el cohete.', 'two':'👀 No ha despegado el cohete.'},'answer_options': {'one':'game_one_op_one', 'two':'game_one_op_two'}}
                },
                'two': {
                    'description': 'Juego 2️⃣.\nPregunta: ¿La imagen pertenece al lanzamiento?\nOpciones:\n🔹Sí, pertenece: proporciona la fecha del lanzamiento.\n🔹No, pero ya ha despegado el cohete: sigue jugando.\n🔹No, no ha despegado: sigue jugando.',
                    'option':'Juego 2️⃣',
                    'option_selected': 'two',
                     'options': {'question': '¿La imagen pertenece al lanzamiento?', 
                                 'answer_text': {'one':'✅ Sí, pertenece.', 'two':'🚀 No, pero ya ha despegado el cohete.', 'three':'👀 No, no ha despegado'},
                                 'answer_options': {'one':'game_two_op_one', 'two':'game_two_op_two', 'three':'game_two_op_three'}}
                }
            }
        },
        'en': {
            'languages_options': {
                'welcome': '🇺🇸 Hello! In which language would you like to continue?',
                'button_text': '🇺🇸 English',
                'option': 'en',
                'language_selected': '🇺🇸 You have selected the English language.',
            },
            'game_options': {
                'titles': {
                    'mode_game': '👾Select a game mode.👾',
                    'game_selected': 'You have selected game ',
                    'final_answer' : '🏁The date and time you chose is: ',
                    'release_date' : '🚀The release date and time was:',
                    'correct' : '🚀🥳¡The rocket took off!!🥳🚀',
                    'false' : "🚀😓¡the rocket had not fired!😓🚀\n",
                    'limit' : '😨You have reached the frame limit for this video.😨',
                    'goodbye' : "Thanks for playing, we'll connect soon.\n\n/start"
                },
                'one': {
                    'description': 'Game 1️⃣.\nQuestion: Has the rocket been launched yet?\nOptions:\n🔹Yes: provides release date.\n🔹No: keep playing.',
                    'option':'Game 1️⃣',
                    'option_selected': 'one',
                    'options': {'question': 'Has the rocket been launched yet?', 'answer_text': {'one':'🚀 Yes, the rocket has already taken off', 'two':'👀 The rocket has not taken off'},'answer_options': {'one':'game_one_op_one', 'two':'game_one_op_two'}}
                },
                'two': {
                    'description': "Game 2️⃣.\nQuestion: Does the frame belong to the launch?\nOptions:\n🔹Yes, it belongs: provides release date.\n🔹No, but the rocket has already taken off: keep playing.\n🔹No, it hasn't taken off: keep playing.",
                    'option':'Game 2️⃣',
                    'option_selected': 'two',
                    'options': {'question': 'Does the image belong to the launch?', 
                                'answer_text': {'one':'✅ Yes, it belongs.', 'two':'🚀 No, but the rocket has already taken off', 'three':"👀 No, it hasn't taken off"},
                                'answer_options': {'one':'game_two_op_one', 'two':'game_two_op_two', 'three':'game_two_op_three'}}
                }
            }
        },
    },
    'messages' : {
        'errorApi': '🚀💥\n🇪🇸 Estamos experimentando algunos problemas en este momento, inténtelo nuevamente más tarde.\n🇺🇸 We are experiencing some issues at the moment, please try again later.',
        'error': '🚀 🇪🇸 Comando no válido, comandos válidos /start o /help\n🇺🇸 Invalid command, valid commands /start or /help',
        'help': '🚀🇪🇸 Un bot interactivo para adivinar los momentos del lanzamiento del cohete en imagen. ¡Diviértete y desafía tus habilidades!\n🚀🇺🇸 An interactive bot to guess the launch moments of the rocket in a frame. Have fun and challenge your skills!\n/start'
    }
        
}