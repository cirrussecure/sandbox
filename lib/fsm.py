
# $ 2to3 fsm.py -w

__version__ = "$Id: $"


# -------------------------------------------------------------------
# imports

import time

#
# -----------------------------------------------

class Fsm():
    '''
    '''

    def __init__(self, trace = None):
        '''
        leading double underscores make these
        private (i.e. prevents name collision
        if sub-classed)
        '''
        if trace == None: trace = 0
        self.__trace = trace
        self.__event = None
        self.__state_next = self.state_initial
        # used by run()
        self.__args = ()

    def state_initial(self, *args):
        if self.__trace >= 1:
            print("Default initial state.\n")

    def state_final(self, *args):
        if self.__trace >= 1:
            print("Default final state.\n")
        # print 'state_final() args: ', args
        return args

    def next(self, *args):
        '''
        '''
        if self.__trace >= 1:
            # print 'State: %s' % (self.next_state().func_name)
            print('State: %s' % (self.__state_next.__name__))
        if self.__trace >= 2: time_of_dispatch = time.clock()
        # print 'next() args: ', args
        result = self.__state_next(*args)
        if self.__trace >= 3:
            time_diff = time.clock() - time_of_dispatch
            print("Duration of state: %f" % (time_diff))
        # print 'next() result: ', result
        return result

    def run(self):
        '''
        '''
        while True:
            # print 'run() args: ', self.__args
            result = self.next(self.__args)
            # print 'run() result: ', result
            # if self.next_state() == self.state_final:
            if self.__state_next == self.state_final:
                break
        result = self.next(*self.__args)
        if self.__trace >= 1:
            print("Returning to parent state.")
        return result

    def next_state(self, state=None, *args):
        '''
        '''
        # print 'next_state() state: ', state
        # print 'next_state() args: ', args
        if state != None:
            self.__state_next = state
        self.__args = args
        return self.__state_next

#
# -------------------------------------------------------------------

# -----------------------------------------------

class FsmExample(Fsm):
    '''
    create test case by sub-classing
    '''

    def __init__(self, trace = None):
        '''
        '''
        Fsm.__init__(self, trace)
        print("\nCreating an instance.\n")
        self.counter_pass = 1

        # ---------------------------------------
        # overide same in Fsm
        # finite state machine starts here
    def state_initial(self, *args):
        print("Initializing.\n")
        self.next_state(self.state_print_time, ('first_call',))
        return args

    def state_print_time(self, *args):
        '''
        '''
        print("Pass: %d " % (self.counter_pass))
        print(args)
        time_pass = time.strftime("%a, %b %d %Y, %H:%M:%S", time.localtime())
        self.time_print(time_pass)
        self.counter_pass = self.counter_pass + 1
        self.next_state(self.state_wait, (self.counter_pass, args,))
        # self.next_state(self.state_wait)
        return args

    def state_wait(self, *args):
        '''
        '''
        print(args)
        print('counter_pass: ', args[0][0][0])
        print("Pausing before next pass.")
        print("Press any key to stop.\n")

        delay_seconds = 2

        # # `tps 20191202 begin delete
        # while (msvcrt.kbhit() == False):
        #     if (delay_seconds > 0):
        #         delay_seconds = delay_seconds - 1
        #         time.sleep(1)
        #     else:
        #         self.next_state(self.state_print_time, ('subsequent_calls',))
        #         # self.next_state(self.state_print_time)
        #         break
        # else:
        #     # ---------------------------------------
        #     # state_final always casues exit to parent
        #     self.next_state(self.state_final)
        # return args
        # # `tps 20191202 end delete
        # `tps 20191202 begin add
        while (True):
            if (delay_seconds > 0):
                delay_seconds = delay_seconds - 1
                time.sleep(1)
            else:
                self.next_state(self.state_print_time, ('subsequent_calls',))
                # self.next_state(self.state_print_time)
                break
        else:
            # ---------------------------------------
            # state_final always casues exit to parent
            self.next_state(self.state_final)
        return args
        # `tps 20191202 end add

    def time_print(self, time):
        print("Time: %s" % (time))

#
# -----------------------------------------------
def main():
    '''
    instantiate and run the test case
    '''

    print(('fsm module test: rev. %s, %s') % (
        __version__.split()[2],
        __version__.split()[3]
    ))
    # fsm = FsmExample(trace=3)
    fsm = FsmExample()
    fsm.run()

# -------------------------------------------------------------------
if __name__ == "__main__":

    # -------------------------------------------
    # import msvcrt
    main()
    # raw_input("Press return to continue")

    # -------------------------------------------
    # following runs pydoc on this module
    # import pydoc; pydoc.writedoc(main)

    # -------------------------------------------
    # following loads main() then shows debug prompt
    # import pdb; pdb.run('main()')

    # -------------------------------------------
    # following act as a break point, it stops
    # execution and shows debug prompt
    # import pdb; pdb.set_trace()


"""
-----------------------------------------------------------
Change history begin:



Change history end:
-----------------------------------------------------------
About finite state machines (FSM's):

For more about finite state machines (FSM's) versus hierarchical state
machines (HSM's) see the excerpt below which is taken from section 2.3 of
this book:

'Practical UML Statecharts in C/C++Event-Driven Programming for Embedded
Systems' by Miro Samek
Publisher: Newnes
Pub Date: October 01, 2008
Print ISBN-10: 0-7506-8706-1
Print ISBN-13: 978-0-7506-8706-5
Pages: 728


2.3. UML Extensions to the Traditional FSM Formalism

Though the traditional FSMs are an excellent tool for tackling smaller
problems, it's also generally known that they tend to become unmanageable,
even for moderately involved systems. Due to the phenomenon known as state
explosion, the complexity of a traditional FSM tends to grow much faster
than the complexity of the reactive system it describes. This happens
because the traditional state machine formalism inflicts repetitions. For
example, if you try to represent the behavior of the Visual Basic
calculator introduced in Section 2.1 with a traditional FSM, you'll
immediately notice that many events (e.g., the Clear event) are handled
identically in many states. A conventional FSM, however, has no means of
capturing such a commonality and requires repeating the same actions and
transitions in many states. What's missing in the traditional state
machines is the mechanism for factoring out the common behavior in order
to share it across many states.

The formalism of statecharts, invented by David Harel in the 1980s [Harel
87], addresses exactly this shortcoming of the conventional FSMs.
Statecharts provide a very efficient way of sharing behavior so that the
complexity of a statechart no longer explodes but tends to faithfully
represent the complexity of the reactive system it describes. Obviously,
formalism like this is a godsend to embedded systems programmers (or any
programmers working with event-driven systems) because it makes the state
machine approach truly applicable to real-life problems.

UML state machines, known also as UML statecharts [OMG 07], are
object-based variants of Harel statecharts and incorporate several
concepts defined in ROOMcharts, a variant of the statechart defined in the
Real-time Object-Oriented Modeling (ROOM) language [Selic+ 94]. UML
statecharts are extended state machines with characteristics of both Mealy
and Moore automata. In statecharts, actions generally depend on both the
state of the system and the triggering event, as in a Mealy automaton.
Additionally, UML statecharts provide optional entry and exit actions,
which are associated with states rather than transitions, as in a Moore
automaton.

"""
