from src.analysis import get_search_term, evaluate_search_term

if __name__ == '__main__':
    st = get_search_term()
    evaluate_search_term(search_term=st['search_term'], location=st['location'])
    print('Ran on update')
