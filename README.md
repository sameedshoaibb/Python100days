from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        H1 = self.addHost( 'h1' )
        H2 = self.addHost( 'h2' )
        H3 = self.addHost( 'h3' )
        H4 = self.addHost( 'h4' )
        H5 = self.addHost( 'h5' )

        S1 = self.addSwitch( 's1' )
        S2 = self.addSwitch( 's2' )
        S3 = self.addSwitch( 's3' )
        S4 = self.addSwitch( 's4' )
        S5 = self.addSwitch( 's5' )
        S6 = self.addSwitch( 's6' )
        S7 = self.addSwitch( 's7' )
        S8 = self.addSwitch( 's8' )
        S9 = self.addSwitch( 's9' )
        S10 = self.addSwitch( 's10' )


        # Add links
        self.addLink( H1, S1 )
        self.addLink( H2, S2 )
        self.addLink( H3, S3 )
        self.addLink( H4, S9 )
        self.addLink( H5, S10 )
        self.addLink( S4, S3 )
        self.addLink( S4, S2 )
        self.addLink( S4, S1 )
        self.addLink( S4, S5 )
        self.addLink( S4, S6 )
        self.addLink( S5, S7 )
        self.addLink( S6, S8 )
        self.addLink( S7, S8 )
        self.addLink( S7, S9 )
        self.addLink( S9, S10 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
