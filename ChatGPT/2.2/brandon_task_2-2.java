package nl.tudelft.jpacman.npc.ghost;

import nl.tudelft.jpacman.board.Direction;
import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.sprite.Sprite;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * Test class for the Blinky class, which represents the red ghost in Pac-Man.
 * This test suite checks Blinky's movement logic, ensuring it can randomly 
 * move to accessible squares and handles invalid movement directions (like walls).
 */
public class BlinkyTest {

    private Blinky blinky;
    private Square square;

    /**
     * Sets up the environment before each test. Initializes Blinky and 
     * creates a mock Square that simulates the board's behavior.
     * The square is set to contain Blinky, and surrounding squares 
     * are mocked to represent directions (NORTH, SOUTH, EAST, WEST).
     */
    @BeforeEach
    void setUp() {
        Map<Direction, Sprite> spriteMap = new HashMap<>();
        blinky = new Blinky(spriteMap);
        square = mock(Square.class);

        // Mock the behavior of the square: it returns itself as being occupied by Blinky
        when(square.getOccupants()).thenReturn(Collections.singletonList(blinky));
        
        // Mock neighboring squares for each direction
        when(square.getSquareAt(Direction.NORTH)).thenReturn(mock(Square.class));
        when(square.getSquareAt(Direction.SOUTH)).thenReturn(mock(Square.class));
        when(square.getSquareAt(Direction.EAST)).thenReturn(mock(Square.class));
        when(square.getSquareAt(Direction.WEST)).thenReturn(mock(Square.class));

        // Place Blinky on the current square
        blinky.occupy(square);
    }

    /**
     * Test case to verify that Blinky can randomly move to an accessible square.
     * Blinky should be able to move to either the NORTH or SOUTH square when both 
     * are accessible, and the chosen direction must be valid (within those options).
     */
    @Test
    void testRandomMove() {
        Square northSquare = mock(Square.class);
        Square southSquare = mock(Square.class);

        // Mock the NORTH and SOUTH squares to be accessible to Blinky
        when(square.getSquareAt(Direction.NORTH)).thenReturn(northSquare);
        when(square.getSquareAt(Direction.SOUTH)).thenReturn(southSquare);
        when(northSquare.isAccessibleTo(blinky)).thenReturn(true);
        when(southSquare.isAccessibleTo(blinky)).thenReturn(true);

        // Define the expected directions Blinky can choose from
        List<Direction> accessibleDirections = Arrays.asList(Direction.NORTH, Direction.SOUTH);

        // Blinky should randomly move to one of the accessible directions
        Direction move = blinky.randomMove();
        assertThat(accessibleDirections).contains(move);
    }

    /**
     * Test case to verify that Blinky returns null when no neighboring squares 
     * are accessible. This simulates Blinky being surrounded by walls, where 
     * no movement is possible.
     */
    @Test
    void testRandomMoveNoAccessibleDirections() {
        // Mock all neighboring squares (in all directions) as inaccessible to Blinky
        for (Direction direction : Direction.values()) {
            Square mockSquare = mock(Square.class);
            when(square.getSquareAt(direction)).thenReturn(mockSquare);
            when(mockSquare.isAccessibleTo(blinky)).thenReturn(false);
        }

        // Since no directions are accessible, Blinky's move should return null
        Direction move = blinky.randomMove();
        assertThat(move).isNull();
    }
}