"""Test multiballs and multiball_locks."""
from mpf.tests.MpfGameTestCase import MpfGameTestCase


class TestMultiBallStackedTrad(MpfGameTestCase):

    def get_config_file(self):
        return 'config.yaml'

    def get_machine_path(self):
        return 'tests/machine_files/multiball_stacked_trad/'

    def get_platform(self):
        return 'smart_virtual'

    def testStackedMultiball(self):
      
        # prepare game this is a 5 ball game
        self.fill_troughs()
        self.assertFalse(self.machine.multiballs["mb1"].enabled)
        self.assertFalse(self.machine.multiballs["mb2"].enabled)

        # start game
        self.start_game()

        # this mode contains the two 3-ball lock devices for multiball
        self.post_event("start_mode1")

        # enable both MBs
        self.post_event("mb1_enable")
        self.assertTrue(self.machine.multiballs["mb1"].enabled)
        self.assertEqual(0, self.machine.multiballs["mb1"].balls_added_live)
        self.post_event("mb2_enable")
        self.assertTrue(self.machine.multiballs["mb2"].enabled)
        self.assertEqual(0, self.machine.multiballs["mb2"].balls_added_live)

        self.advance_time_and_run(4)
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(1, self.machine.playfield.balls)

        ####  First MB is ok *****

        # lock one ball, another should should go to the playfield from the trough (6.001)
        self.hit_switch_and_run("s_lockA1", 10)
        self.assertEqual(1, self.machine.ball_devices["bd_lockA"].balls)
        self.assertEqual(1, self.machine.playfield.balls)

        # lock second ball and another one should go to pf (16.001)
        self.hit_switch_and_run("s_lockA2", 10)
        self.assertEqual(2, self.machine.ball_devices["bd_lockA"].balls)
        self.assertEqual(1, self.machine.playfield.balls)

        # lock third ball all should be released from the lock, and not the trough(26.001)
        self.hit_switch_and_run("s_lockA3", 15)
        self.assertEqual(0, self.machine.ball_devices["bd_lockA"].balls)
        self.assertEqual(3, self.machine.playfield.balls)

        self.advance_time_and_run(1)

        # drain ball (@42.001)
        self.drain_one_ball()

        self.advance_time_and_run(10)
        # At this point I would expect the ball to just drain, and leave 2 balls in play
        # this makes the error more clear below
        self.assertEqual(2, self.machine.playfield.balls)

    
        #### Now do a stacked multiball ######
        # The story so far, a 2 ball multiball is running (from an "add 2 multiball") 
        # where one ball is lost.

        # lock one ball in second ball lock, another should should go to the playfield from the trough 52.001)
        self.hit_switch_and_run("s_lockB1", 10)
        self.assertEqual(1, self.machine.ball_devices["bd_lockB"].balls)
        self.assertEqual(2, self.machine.playfield.balls)

        # lock second ball and another one should go to pf from the trough (62.001)
        self.hit_switch_and_run("s_lockB2", 10)
        self.assertEqual(2, self.machine.ball_devices["bd_lockB"].balls)
        self.assertEqual(2, self.machine.playfield.balls)

        # lock third ball, starting multiball, all balls should be released from the second lock (72.001)
        # resulting in 4 balls on the playfield. 

        self.hit_switch_and_run("s_lockB3", 15)
        self.assertEqual(0, self.machine.ball_devices["bd_lockB"].balls)
        self.assertEqual(4, self.machine.playfield.balls)  # Make sure no extra balls show up


