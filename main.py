from bootstrapper import bootstrapper


def main():
    for step in bootstrapper.initialize_enrichment_steps():
        step.process_step()


if __name__ == '__main__':
    main()
