// Some of my tests from the TDD JPacman lab
package nl.tudelft.jpacman.npc.ghost;

import nl.tudelft.jpacman.board.Board;
import nl.tudelft.jpacman.board.BoardFactory;
import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.level.*;
import nl.tudelft.jpacman.points.DefaultPointCalculator;
import nl.tudelft.jpacman.sprite.PacManSprites;
import org.checkerframework.checker.units.qual.C
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

public class ClydeTest {

    /**
     * Tests that Clyde can find a valid move on a simple map.
     */
    @Test
    void testNextAiMove() {
        // Initialize game sprites and factories needed to create the game level.
        PacManSprites sprites = new PacManSprites();
        LevelFactory levelFactory = new LevelFactory(
            sprites,
            new GhostFactory(sprites),
            new DefaultPointCalculator());
        PlayerFactory playerFactory = new PlayerFactory(new PacManSprites());
        MapParser parser = new MapParser(levelFactory, new BoardFactory(sprites));

        // Create a simple map with an empty square and a Pac-Man.
        Level level = parser.parseMap(new char[][]{{' '}, {'P'}});
        level.registerPlayer(playerFactory.createPacMan());

        // Get the board from the level.
        Board board = level.getBoard();
        
        // Create Clyde and occupy the starting square (0, 0).
        Clyde c = new Clyde(sprites.getGhostSprite(GhostColor.CYAN));
        c.occupy(board.squareAt(0, 0));

        // Verify that Clyde can find a move.
        assertThat(c.nextAiMove().isPresent()).isTrue();
    }

    /**
     * Tests that Clyde cannot move when surrounded by walls.
     */
    @Test
    void testRandomMoveNull() {
        // Initialize game sprites and factories for creating the level.
        PacManSprites sprites = new PacManSprites();
        LevelFactory levelFactory = new LevelFactory(
            sprites,
            new GhostFactory(sprites),
            new DefaultPointCalculator());
        MapParser parser = new MapParser(levelFactory, new BoardFactory(sprites));

        // Create a map with walls surrounding Clyde.
        Level level = parser.parseMap(new char[][]{{'#', '#', '#'}, 
                                                     {'#', ' ', '#'}, 
                                                     {'#', '#', '#'}});
        Board board = level.getBoard();
        
        // Create Clyde and occupy the center square (1, 1).
        Clyde c = new Clyde(sprites.getGhostSprite(GhostColor.CYAN));
        c.occupy(board.squareAt(1, 1));

        // Verify that Clyde cannot move.
        assertThat(c.randomMove()).isNull();
    }
}
