import click
from calc_logic import calculate_volume


@click.command()
@click.argument('current_conf', type=click.FLOAT)
@click.argument('current_area', type=click.FLOAT)
@click.argument('desired_conf', type=click.FLOAT)
@click.argument('dest_area', type=click.FLOAT)
@click.argument('current_vol', type=click.FLOAT)
def main(current_conf, current_area, desired_conf, dest_area, current_vol):
    """
    Calculate the volume to transfer from a source plate to reach desired confluency.
    
    This tool calculates how much volume (in µL) you need to take from a source plate
    of cultured cells to achieve a target confluency in a destination plate.
    
    \b
    ARGUMENTS:
    
    \b
    CURRENT_CONF: Current confluency (%) of the source plate
                  Example: 50 (for 50% confluency)
                  Must be greater than 0
    
    \b
    CURRENT_AREA: Surface area (cm²) of the source plate
                  Example: 60 (for a 10 cm plate)
                  Common values: 0.33 (96-well), 2 (24-well), 4 (12-well), 
                                 10 (6-well), 60 (10 cm dish)
                  Must be greater than 0
    
    \b
    DESIRED_CONF: Target confluency (%) for the destination plate
                  Example: 25 (for 25% confluency)
                  Must be greater than 0
    
    \b
    DEST_AREA: Surface area (cm²) of the destination plate
               Example: 10 (for a 6-well plate)
               Common values: 0.33 (96-well), 2 (24-well), 4 (12-well), 
                              10 (6-well), 60 (10 cm dish)
               Must be greater than 0
    
    \b
    CURRENT_VOL: Total volume (µL) in the source plate after trypsinization
                 Example: 3000 (for 3000 µL)
                 Must be greater than 0
    
    \b
    EXAMPLE:
    
        python cell_volume_cli.py 50 60 25 10 3000
    
    This calculates the volume to take from a 10 cm plate (60 cm²) with 50% 
    confluency to achieve 25% confluency in a 6-well plate (10 cm²), 
    assuming 3000 µL total volume in the source plate.
    """
    try:
        v_take = calculate_volume(current_conf, current_area, desired_conf, dest_area, current_vol)
        
        if v_take > current_vol:
            click.echo(f"Warning: required volume ({v_take:.2f} µL) exceeds available volume ({current_vol:.2f} µL).")
        else:
            click.echo(f"You should take {v_take:.2f} µL from the current plate.")
            
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
