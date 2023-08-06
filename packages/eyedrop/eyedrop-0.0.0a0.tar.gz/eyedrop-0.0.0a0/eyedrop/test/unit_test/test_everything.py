from eyedrop import src


def test_welcome_message():
	assert src.welcome_message() == 'Welcome to Eyedrop!'
