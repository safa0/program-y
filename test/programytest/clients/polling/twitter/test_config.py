import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class TwitterConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              polling_interval: 59
              rate_limit_sleep: 900
              use_status: true
              use_direct_message: true
              auto_follow: true
              welcome_message: Thanks for following me
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(59, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)
        self.assertTrue(twitter_config.use_status)
        self.assertTrue(twitter_config.use_direct_message)
        self.assertTrue(twitter_config.auto_follow)
        self.assertEqual("Thanks for following me", twitter_config.welcome_message)

    def test_init_no_auto_follow(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              polling_interval: 59
              rate_limit_sleep: 900
              use_status: true
              use_direct_message: false
              auto_follow: false
              welcome_message: Thanks for following me
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(59, twitter_config.polling_interval)
        self.assertEqual(900, twitter_config.rate_limit_sleep)
        self.assertTrue(twitter_config.use_status)
        self.assertFalse(twitter_config.use_direct_message)
        self.assertFalse(twitter_config.auto_follow)
        self.assertEqual("Thanks for following me", twitter_config.welcome_message)

    def test_to_yaml_with_defaults(self):
        config = TwitterConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['polling_interval'], 0)
        self.assertEqual(data['rate_limit_sleep'], -1)
        self.assertEqual(data['use_status'], False)
        self.assertEqual(data['use_direct_message'], False)
        self.assertEqual(data['auto_follow'], False)
        self.assertEqual(data['welcome_message'], "Thanks for following me.")

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])

    def test_to_yaml_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            other:
        """, ConsoleConfiguration(), ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_configuration(yaml, ".")

        self.assertEqual(0, twitter_config.polling_interval)
        self.assertEqual(-1, twitter_config.rate_limit_sleep)
        self.assertFalse(twitter_config.use_status)
        self.assertFalse(twitter_config.use_direct_message)
        self.assertFalse(twitter_config.auto_follow)
        self.assertEqual("Thanks for following me.", twitter_config.welcome_message)
