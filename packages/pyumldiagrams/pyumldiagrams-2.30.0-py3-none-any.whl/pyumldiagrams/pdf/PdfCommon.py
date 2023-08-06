from typing import Tuple

from pyumldiagrams.Common import Common
from pyumldiagrams.Definitions import Position

from pyumldiagrams.Defaults import LEFT_MARGIN
from pyumldiagrams.Defaults import TOP_MARGIN

from pyumldiagrams.Internal import InternalPosition
from pyumldiagrams.Internal import PolygonPoints
from pyumldiagrams.Internal import ScanPoints


class PdfCommon(Common):

    @classmethod
    def toPdfPoints(cls, pixelNumber: float, dpi: int) -> int:
        """

        points = pixels * 72 / DPI

        Args:
            pixelNumber:  From the display
            dpi:  dots per inch of source display

        Returns:  A pdf point value to use to position on a generated document

        """
        points: int = int((pixelNumber * 72)) // dpi

        return points

    @classmethod
    def convertPosition(cls, pos: Position, dpi: int, verticalGap: float, horizontalGap: float) -> Tuple[float, float]:

        x: float = PdfCommon.toPdfPoints(pos.x, dpi) + LEFT_MARGIN + verticalGap
        y: float = PdfCommon.toPdfPoints(pos.y, dpi) + TOP_MARGIN + horizontalGap

        return x, y

    @classmethod
    def pointInsidePolygon(cls, pos: InternalPosition, polygon: PolygonPoints) -> bool:
        """
        Based on this: http://www.ariel.com.au/a/python-point-int-poly.html

        Args:
            pos: The position to check
            polygon: The polygon

        Returns: True if it is, else False
        """
        x: float = pos.x
        y: float = pos.y
        n: int   = len(polygon)

        inside: bool = False

        p1: InternalPosition = polygon[0]
        p1x: float = p1.x
        p1y: float = p1.y

        for i in range(n + 1):
            p2: InternalPosition = polygon[i % n]
            p2x: float = p2.x
            p2y: float = p2.y

            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        xIntersection: float = 0
                        if p1y != p2y:
                            xIntersection: float = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xIntersection:
                            inside = not inside

            p1x = p2x
            p1y = p2y

        return inside

    @classmethod
    def buildScanPoints(cls, points: PolygonPoints) -> ScanPoints:

        minX: float = points[0].x
        maxX: float = points[0].y
        minY: float = points[0].x
        maxY: float = points[0].y

        for point in points:
            currX: float = point.x
            currY: float = point.y
            if currX < minX:
                minX = currX
            if currX > maxX:
                maxX = currX

            if currY < minY:
                minY = currY
            if currY > maxY:
                maxY = currY

        scanPoints: ScanPoints = ScanPoints()

        scanPoints.startScan = InternalPosition(minX, minY)
        scanPoints.endScan   = InternalPosition(maxX, maxY)

        return scanPoints
