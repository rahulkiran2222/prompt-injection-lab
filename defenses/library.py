class DefenseProtocols:
    @staticmethod
    def no_defense(user_input):
        return user_input

    @staticmethod
    def xml_tagging(user_input):
        """Wraps user input in XML tags to help the model distinguish instructions."""
        return f"<user_input>\n{user_input}\n</user_input>"

    @staticmethod
    def delimiter_guard(user_input):
        """Adds clear delimiters."""
        return f"### USER INPUT START ###\n{user_input}\n### USER INPUT END ###"
