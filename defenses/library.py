class DefenseProtocols:
    @staticmethod
    def no_defense(user_input):
        return user_input

    @staticmethod
    def xml_tagging(user_input):
        return f"<user_input>\n{user_input}\n</user_input>"

    @staticmethod
    def delimiter_guard(user_input):
        return f"### START INPUT ###\n{user_input}\n### END INPUT ###"
