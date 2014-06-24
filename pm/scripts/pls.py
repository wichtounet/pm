from pm.projects import list_projects

def main():

    projects = list_projects()

    for p in projects:
        print(p)

    print("")
    print("{} projects".format(len(projects)))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))