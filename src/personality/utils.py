
def clear_test_session(request):
    try:
        del request.session['done_o']
        del request.session['done_c']
        del request.session['done_e']
        del request.session['done_a']
        del request.session['done_n']
        del request.session['avg_o']
        del request.session['avg_c']
        del request.session['avg_e']
        del request.session['avg_a']
        del request.session['avg_n']
    except KeyError:
        print('KeyError')
        return False

    return True
