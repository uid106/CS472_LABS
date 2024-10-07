// Some of my tests from the tdd jpacman lab
package nl.tudelft.jpacman.npc.ghost;

import nl.tudelft.jpacman.board.Board;
import nl.tudelft.jpacman.board.BoardFactory;
import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.level.*;
import nl.tudelft.jpacman.points.DefaultPointCalculator;
import nl.tudelft.jpacman.sprite.PacManSprites;
import org.checkerframework.checker.units.qual.C;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

public class ClydeTest {
    /**
     * Verifies that Clyde can find a move
     */
    @Test
    void testNextAiMove() {
        PacManSprites sprites = new PacManSprites();
        LevelFactory levelFactory = new LevelFactory(
            sprites,
            new GhostFactory(sprites),
            new DefaultPointCalculator());
        PlayerFactory playerFactory = (new PlayerFactory(new PacManSprites()));
        MapParser parser = new MapParser(levelFactory, new BoardFactory(sprites));
        Level level = parser.parseMap(new char[][]{{' '}, {'P'}});
        level.registerPlayer(playerFactory.createPacMan());
        Board board = level.getBoard();
        Clyde c = new Clyde(sprites.getGhostSprite(GhostColor.CYAN));

        c.occupy(board.squareAt(0,0));
        assertThat(c.nextAiMove().isPresent()).isTrue();
    }

    /**
     * Verifies that a Clyde surrounded by inaccessible squares cannot move
     */
    @Test
    void testRandomMoveNull() {
        PacManSprites sprites = new PacManSprites();
        LevelFactory levelFactory = new LevelFactory(
            sprites,
            new GhostFactory(sprites),
            new DefaultPointCalculator());
        MapParser parser = new MapParser(levelFactory, new BoardFactory(sprites));
        Level level = parser.parseMap(new char[][]{{'#', '#', '#'}, {'#', ' ', '#'}, {'#', '#', '#'}});
        Board board = level.getBoard();
        Clyde c = new Clyde(sprites.getGhostSprite(GhostColor.CYAN));
        c.occupy(board.squareAt(1,1));

        assertThat(c.randomMove()).isNull();
    }
}
