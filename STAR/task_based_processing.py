import numpy as np
import sys
import inspect
# Note MPI_Init is called when mpi4py is imported.
# MPI_Finalize is called when the script ends.
from mpi4py import MPI


def initialize_mpi(debug=False):
    
    # Initialize MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    if (debug): print "Size =", size
    if (debug): print "Rank =", rank

    return rank, size, comm

def send_data(data_chunk, destination, comm, tag=0):
    # Here we don't know what type of object
    # the work is, so we use the generic send.
    comm.send(data_chunk, dest=destination, tag=tag)

    return

def wait_for_message(recv_buff, status, comm, debug=False):
    # Wait for a request for
    # the next instruction.
    # Generally the root is waiting
    # for a request for more work
    # from a worker.

    if (debug): print "Root in wait_for_message"
    comm.Recv(recv_buff, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
    source = status.Get_source()
    tag    = status.Get_tag()
    if (debug):
        print "source=", source
        print "tag=", tag

    return recv_buff, source, tag

def ask_for_work(msg, destination, comm, tag=0):

    comm.Send([msg, 1, MPI.INT], destination, tag=tag)

    return

def process_data(local_data, pre, fancy=''):

    for thing in local_data:
        print pre, fancy, thing

    return

def get_chunk(all_data, current_index, chunk_size):

    ci = current_index
    pi = min(chunk_size, len(all_data[ci:]))
    chunk = all_data[ci:ci+pi]
    new_index = ci+pi
    return chunk, new_index

def needs_current_index_arg(function):
    #See https://stackoverflow.com/questions/196960/
    #    can-you-list-the-keyword-arguments-a-function-receives 
    args, varargs, varkw, defaults = inspect.getargspec(function)
    return ('current_index' in args)


def perform_task_in_parallel(function, args, kwargs, all_data,
                             chunk_size, rank, size, comm,
                             root=0, debug=False):

    """
    Perform a function on all_data
    in parallel. This breaks the data up
    into chunks on the root processor, who
    then hands out the chunks to the other
    processors as soon as they are free to
    do the work.
    This task based parallel programming
    ensures that all processors are always
    busy, unlike data parallelization.
    Note the work function takes args and kwargs
    in the form of 
    function(local_data, *args, **kwargs)
    where local_data is the chunk sent by
    the root, args is a list of arguments
    to be unrolled in passing, and **kwargs
    is a dictionary of {'kw':'arg'} pairs
    that is unrolled to kw=arg in the
    function call.
    """

    pre = "Proc", rank

    if (debug): print pre, "Entering perform_task_in_parallel."
    
    # Keep a status object around for async comms
    status = MPI.Status()

    # Note sending and recieving numpy
    # arrays is faster than the object
    # method with mpi4py.
    send_me_work = np.array([999], dtype=int)
    everyone_all_done = np.array([100], dtype=int)
    recv_buff  = np.zeros(1, dtype=int)
    work_tag = 999
    done_tag = 100
    
    # For keeping track of who's
    # currently doing what, we use an integer
    # array called procs_status.
    idle    = 200
    working = 999
    done    = 100
    # Everyone starts idle.
    procs_status = np.zeros(size-1)
    procs_status[:] = idle

    not_done = True
    current_index = 0

    counter = 0
    frac_done = 0.

    comm.Barrier()

    if (rank == root):
        number_of_work_units = len(all_data)
        last_data_index = len(all_data)-1
        procs_status[:] = working

    if (rank == root): # I'm the supervisor
        # Check to see if any procs are still active.
        while (np.array(procs_status != done).any()):
            
            # Progress tracker (at least on the root processor).
            if ( int((float(counter) 
                 / float(number_of_work_units)
                 / float(chunk_size))*100.) >= frac_done):
                print "Progress at {:.0f} %".format(frac_done)
                frac_done += 3.

            # Wait for someone to say they want some work.
            if (debug): print pre, "Waiting for message asking for work."
            recv_buff, source, tag = wait_for_message(recv_buff, status,
                                                      comm, debug=debug)
            if (debug): print pre, "recieved", recv_buff, "from", source
            
            if (not_done):
                # Get a chunk of data
                if (debug): print pre, "Getting data chunk."
                data_chunk, new_index = \
                    get_chunk(all_data, current_index, chunk_size)
            
            # Who did we recieve from, and are they ready for work?
            if (recv_buff == send_me_work and not_done):
                # Tell this processor we are about to send some
                # work.
                comm.Send([send_me_work, 1, MPI.INT],
                           dest=source, tag=current_index)
                # Send the work
                if (debug): print pre, "Sending", source, "work =", data_chunk
                send_data(data_chunk, source, comm, tag=current_index)
                procs_status[source-1] = working
            else:
                # Tell this proc we're done.
                if (debug): print pre, "Telling", source, "we're done."
                comm.Send([everyone_all_done,  MPI.INT], dest=source, tag=done_tag)
                procs_status[source-1] = done
                if (debug): print pre, "proc_status array =", procs_status
            
            current_index = new_index
            if (current_index > last_data_index):
                not_done = False

            counter += 1

            if (debug): print "Counter = ", counter

    else: # I'm a worker bee.

        while not_done:

            # Ask the root for more work.
            if (debug): print pre, "Asking root for work."
            comm.Send([send_me_work, 1, MPI.INT], dest=root, tag=0)
            # Wait for a reply, then check the reply size
            # to determine if this is work or just a message
            # tell us we are all done.
            if (debug):
                print pre, "Getting message about if we are done."
                # For serious debugging, uncomment these lines.
                comm.Probe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG, status=status)
                print pre, "source = ", status.Get_source()
                print pre, "tag    = ", status.Get_tag()
                print pre, "count  = ", status.Get_elements(MPI.INT)
                print pre, "size   = ", status.Get_count()
            comm.Recv([recv_buff, MPI.INT], source=root,
                       tag=MPI.ANY_TAG, status=status)
            tag   = status.Get_tag()
            if (debug): print pre, "Message tag =", tag
            if (recv_buff != done_tag):
                # Its a data object, just use a regular recieve.
                if (debug): print pre, "Getting data from root."
                local_data = comm.recv(source=root, tag=tag, status=status)
                if (debug): print pre, "Processing data from root."
                if (needs_current_index_arg(function)):
                    kwargs['current_index']=tag
                if (debug): print "kwargs=", kwargs
                function(local_data, *args, **kwargs)
            else:
                # Otherwise its a simple one count array message. Recieve that.
                if (debug): print pre, "Got non-data message from root."
                # Not used now that we explicitly communicate a message
                # about work status before we send the work chunk.
                #comm.Recv(recv_buff, source=root, tag=MPI.ANY_TAG, status=status)
                if (debug): print pre, "Root sent", recv_buff
                if (recv_buff == everyone_all_done):
                    not_done = False
                    if (debug):
                        print pre, "Hears from root we're all done."

    
    print pre, "Exiting from perform_task_in_parallel"
    return

def test_task_based_mpi(debug):
    
    rank, size, comm = initialize_mpi(debug=debug)

    root = 0
    all_data = None
    chunk_size = None

    if (rank == root):
        all_data = np.arange(10)
        chunk_size = 3

    pre = "Proc", rank
    args = [pre]
    kwargs = {'fancy':'very fancy'}

    perform_task_in_parallel(process_data, args, kwargs,
                             all_data, chunk_size, 
                             rank, size, comm, debug=debug)

    print "We're all done here."

if (__name__ == '__main__'):
    debug = False
    test_task_based_mpi(debug)
