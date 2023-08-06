//
//  Grid3Drcdsp.h
//  ttcr
//
//  Created by Bernard Giroux on 2018-11-23.
//  Copyright © 2018 Bernard Giroux. All rights reserved.
//

#ifndef Grid3Drcdsp_h
#define Grid3Drcdsp_h

#ifdef VTK
#include "vtkPoints.h"
#include "vtkPolyData.h"
#include "vtkSmartPointer.h"
#include "vtkXMLPolyDataWriter.h"
#endif

#include "Grid3Drc.h"
#include "Node3Dc.h"
#include "Node3Dcd.h"

namespace ttcr {
    
    template<typename T1, typename T2, typename CELL>
    class Grid3Drcdsp : public Grid3Drc<T1,T2,Node3Dc<T1,T2>,CELL> {
    public:
        Grid3Drcdsp(const T2 nx, const T2 ny, const T2 nz,
                    const T1 ddx, const T1 ddy, const T1 ddz,
                    const T1 minx, const T1 miny, const T1 minz,
                    const T2 ns, const bool ttrp, const T2 nd, const T1 drad,
                    const size_t nt=1) :
        Grid3Drc<T1,T2,Node3Dc<T1,T2>,CELL>(nx, ny, nz, ddx, ddy, ddz, minx, miny, minz, ttrp, nt),
        nSecondary(ns), nTertiary(nd), nPermanent(0),
        dynRadius(drad),
        tempNodes(std::vector<std::vector<Node3Dcd<T1,T2>>>(nt)),
        tempNeighbors(std::vector<std::vector<std::vector<T2>>>(nt))
        {
            buildGridNodes();
            this->template buildGridNeighbors<Node3Dc<T1,T2>>(this->nodes);
            nPermanent = static_cast<T2>(this->nodes.size());
            for ( size_t n=0; n<nt; ++n ) {
                tempNeighbors[n].resize(this->ncx * this->ncy * this->ncz);
            }
        }
        
        ~Grid3Drcdsp() {
        }

    private:
        T2 nSecondary;                 // number of permanent secondary
        T2 nTertiary;                   // number of temporary secondary
        T2 nPermanent;                 // total nb of primary & permanent secondary
        T1 dynRadius;

        // we will store temporary nodes in a separate container.  This is to
        // allow threaded computations with different Tx (location of temp
        // nodes vary from one Tx to the other)
        mutable std::vector<std::vector<Node3Dcd<T1,T2>>> tempNodes;
        mutable std::vector<std::vector<std::vector<T2>>> tempNeighbors;

        void buildGridNodes();
        void addTemporaryNodes(const std::vector<sxyz<T1>>&, const size_t) const;

        void initQueue(const std::vector<sxyz<T1>>& Tx,
                       const std::vector<T1>& t0,
                       std::priority_queue<Node3Dc<T1,T2>*,
                       std::vector<Node3Dc<T1,T2>*>,
                       CompareNodePtr<T1>>& queue,
                       std::vector<Node3Dcd<T1,T2>>& txNodes,
                       std::vector<bool>& inQueue,
                       std::vector<bool>& frozen,
                       const size_t threadNo) const;
        
        void propagate(std::priority_queue<Node3Dc<T1,T2>*,
                       std::vector<Node3Dc<T1,T2>*>,
                       CompareNodePtr<T1>>& queue,
                       std::vector<bool>& inQueue,
                       std::vector<bool>& frozen,
                       const size_t threadNo) const;
        
        void raytrace(const std::vector<sxyz<T1>>&,
                      const std::vector<T1>&,
                      const std::vector<sxyz<T1>>&,
                      const size_t=0) const;
        
        void raytrace(const std::vector<sxyz<T1>>&,
                      const std::vector<T1>&,
                      const std::vector<const std::vector<sxyz<T1>>*>&,
                      const size_t=0) const;
    };

    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::buildGridNodes() {


        this->nodes.resize(// secondary nodes on the edges
                           this->ncx*nSecondary*((this->ncy+1)*(this->ncz+1)) +
                           this->ncy*nSecondary*((this->ncx+1)*(this->ncz+1)) +
                           this->ncz*nSecondary*((this->ncx+1)*(this->ncy+1)) +
                           // secondary nodes on the faces
                           (nSecondary*nSecondary)*(this->ncx*this->ncy*(this->ncz+1))+
                           (nSecondary*nSecondary)*(this->ncx*this->ncz*(this->ncy+1))+
                           (nSecondary*nSecondary)*(this->ncy*this->ncz*(this->ncx+1))+
                           // primary nodes
                           (this->ncx+1) * (this->ncy+1) * (this->ncz+1),
                           Node3Dc<T1,T2>(this->nThreads));

        // Create the grid, assign a number for each node and find the owners
        // Nodes and cells are first indexed in z, then y, and x.
        // Secondary nodes are placed on the faces and edges of every cells.
        // Ex: the node in "node[A]=(i,j,k)" is followed by the node in
        // "node[A+1]=(i+dx,j,k)"

        T1 dxs = this->dx/(nSecondary+1);     // distance between secondary nodes in x
        T1 dys = this->dy/(nSecondary+1);
        T1 dzs = this->dz/(nSecondary+1);

        T2 cXmYmZm;     // cell in the (x-,y-,z-) direction from the node
        T2 cXpYmZm;     // cell in the (x+,y-,z-) direction from the node
        T2 cXmYpZm;
        T2 cXpYpZm;
        T2 cXmYmZp;
        T2 cXpYmZp;
        T2 cXmYpZp;
        T2 cXpYpZp;

        T2 n = 0;
        for ( T2 nk=0; nk<=this->ncz; ++nk ) {

            T1 z = this->zmin + nk*this->dz;

            for ( T2 nj=0; nj<=this->ncy; ++nj ) {

                T1 y = this->ymin + nj*this->dy;

                for ( T2 ni=0; ni<=this->ncx; ++ni, ++n ){

                    T1 x = this->xmin + ni*this->dx;

                    // Find the adjacent cells for each primary node

                    if (ni < this->ncx && nj < this->ncy && nk < this->ncz){
                        cXpYpZp = nj*this->ncx + nk*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYpZp = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj < this->ncy && nk < this->ncz){
                        cXmYpZp = nj*this->ncx + nk*(this->ncx*this->ncy) + ni - 1;
                    }
                    else {
                        cXmYpZp = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj > 0 && nk < this->ncz){
                        cXpYmZp = (nj-1)*this->ncx + nk*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYmZp = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj > 0 && nk < this->ncz){
                        cXmYmZp = (nj-1)*this->ncx + nk*(this->ncx * this->ncy) + ni - 1;
                    }
                    else {
                        cXmYmZp = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj < this->ncy && nk > 0){
                        cXpYpZm = nj*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYpZm = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj < this->ncy && nk > 0){
                        cXmYpZm = nj*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni - 1;
                    }
                    else {
                        cXmYpZm = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj > 0 && nk > 0){
                        cXpYmZm = (nj-1)*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYmZm = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj > 0 && nk > 0){
                        cXmYmZm = (nj-1)*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni-1;
                    }
                    else {
                        cXmYmZm = std::numeric_limits<T2>::max();
                    }


                    // Index the primary nodes owners

                    if ( cXmYmZm != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXmYmZm );
                    }
                    if ( cXpYmZm != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXpYmZm );
                    }
                    if ( cXmYpZm != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXmYpZm );
                    }
                    if ( cXpYpZm != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXpYpZm );
                    }
                    if ( cXmYmZp != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXmYmZp );
                    }
                    if ( cXpYmZp != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXpYmZp );
                    }
                    if ( cXmYpZp != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXmYpZp );
                    }
                    if ( cXpYpZp != std::numeric_limits<T2>::max() ) {
                        this->nodes[n].pushOwner( cXpYpZp );
                    }

                    this->nodes[n].setXYZindex( x, y, z, n );

                }
            }
        }

        for ( T2 nk=0; nk<=this->ncz; ++nk ) {

            T1 z = this->zmin + nk*this->dz;

            for ( T2 nj=0; nj<=this->ncy; ++nj ) {

                T1 y = this->ymin + nj*this->dy;

                for ( T2 ni=0; ni<=this->ncx; ++ni ){

                    T1 x = this->xmin + ni*this->dx;

                    // Find the adjacent cells for each primary node

                    if (ni < this->ncx && nj < this->ncy && nk < this->ncz){
                        cXpYpZp = nj*this->ncx + nk*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYpZp = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj < this->ncy && nk < this->ncz){
                        cXmYpZp = nj*this->ncx + nk*(this->ncx*this->ncy) + ni - 1;
                    }
                    else {
                        cXmYpZp = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj > 0 && nk < this->ncz){
                        cXpYmZp = (nj-1)*this->ncx + nk*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYmZp = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj > 0 && nk < this->ncz){
                        cXmYmZp = (nj-1)*this->ncx + nk*(this->ncx * this->ncy) + ni - 1;
                    }
                    else {
                        cXmYmZp = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj < this->ncy && nk > 0){
                        cXpYpZm = nj*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYpZm = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj < this->ncy && nk > 0){
                        cXmYpZm = nj*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni - 1;
                    }
                    else {
                        cXmYpZm = std::numeric_limits<T2>::max();
                    }

                    if (ni < this->ncx && nj > 0 && nk > 0){
                        cXpYmZm = (nj-1)*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni;
                    }
                    else {
                        cXpYmZm = std::numeric_limits<T2>::max();
                    }

                    if (ni > 0 && nj > 0 && nk > 0){
                        cXmYmZm = (nj-1)*this->ncx + (nk-1)*(this->ncx*this->ncy) + ni-1;
                    }
                    else {
                        cXmYmZm = std::numeric_limits<T2>::max();
                    }

                    // Secondary nodes on x edge
                    if ( ni < this->ncx ) {
                        for (T2 ns=0; ns<nSecondary; ++ns, ++n ) {

                            T1 xsv = this->xmin + ni* this->dx + (ns+1)*dxs;

                            if ( cXpYmZm != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYmZm );
                            }
                            if ( cXpYpZm != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYpZm );
                            }
                            if ( cXpYmZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYmZp );
                            }
                            if ( cXpYpZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYpZp );
                            }
                            this->nodes[n].setXYZindex( xsv, y, z, n );
                            this->nodes[n].setPrimary(false);
                        }
                    }

                    // Secondary nodes on y edge
                    if ( nj < this->ncy ) {
                        for (T2 ns=0; ns<nSecondary; ++ns, ++n ) {

                            T1 ysv = this->ymin + nj* this->dy + (ns+1)*dys;

                            if ( cXmYpZm != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXmYpZm );
                            }
                            if ( cXpYpZm != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYpZm );
                            }
                            if ( cXmYpZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXmYpZp );
                            }
                            if ( cXpYpZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYpZp );
                            }
                            this->nodes[n].setXYZindex( x, ysv, z, n );
                            this->nodes[n].setPrimary(false);
                        }
                    }

                    // Secondary nodes on z edge
                    if ( nk < this->ncz ) {
                        for (T2 ns=0; ns<nSecondary; ++ns, ++n ) {

                            T1 zsv = this->zmin + nk* this->dz + (ns+1)*dzs;

                            if ( cXmYmZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXmYmZp );
                            }
                            if ( cXpYmZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYmZp );
                            }
                            if ( cXmYpZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXmYpZp );
                            }
                            if ( cXpYpZp != std::numeric_limits<T2>::max() )
                            {
                                this->nodes[n].pushOwner( cXpYpZp );
                            }
                            this->nodes[n].setXYZindex( x, y, zsv, n );
                            this->nodes[n].setPrimary(false);
                        }
                    }

                    // Secondary nodes on the xy0 planes
                    if ( ni < this->ncx && nj < this->ncy ) {
                        for ( T2 sy=0; sy < nSecondary; ++sy ) {
                            for ( T2 sx=0; sx < nSecondary; ++sx, n++ ) {

                                T1 ysv = this->ymin+ nj* this->dy+ (sy+1)*dys;
                                T1 xsv = this->xmin+ ni* this->dx+ (sx+1)*dxs;

                                if ( cXpYpZm != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXpYpZm );
                                }
                                if ( cXpYpZp != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXpYpZp );
                                }
                                this->nodes[n].setXYZindex( xsv, ysv, z, n );
                                this->nodes[n].setPrimary(false);
                            }
                        }
                    }

                    // Secondary nodes on the x0z planes
                    if ( ni < this->ncx && nk < this->ncz ) {
                        for ( T2 sz=0; sz < nSecondary; ++sz ) {
                            for ( T2 sx=0; sx < nSecondary; ++sx, n++ ) {

                                T1 zsv = this->zmin+ nk* this->dz+ (sz+1)*dzs;
                                T1 xsv = this->xmin+ ni* this->dx+ (sx+1)*dxs;

                                if ( cXpYmZp != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXpYmZp );
                                }
                                if ( cXpYpZp != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXpYpZp );
                                }
                                this->nodes[n].setXYZindex( xsv, y, zsv, n );
                                this->nodes[n].setPrimary(false);
                            }
                        }
                    }

                    // Secondary nodes on the 0yz planes
                    if ( nj < this->ncy && nk < this->ncz ) {
                        for ( T2 sz=0; sz < nSecondary; ++sz ) {
                            for ( T2 sy=0; sy < nSecondary; ++sy, n++ ) {

                                T1 zsv = this->zmin+ nk* this->dz+ (sz+1)*dzs;
                                T1 ysv = this->ymin+ nj* this->dy+ (sy+1)*dys;

                                if ( cXmYpZp != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXmYpZp );
                                }
                                if ( cXpYpZp != std::numeric_limits<T2>::max() )
                                {
                                    this->nodes[n].pushOwner( cXpYpZp );
                                }
                                this->nodes[n].setXYZindex( x, ysv, zsv, n );
                                this->nodes[n].setPrimary(false);
                            }
                        }
                    }
                }
            }
        }
        // sanity check
        if ( n != this->nodes.size() ) {
            std::cerr << "Error building grid, wrong number of nodes\n";
            abort();
        }
    }

    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::addTemporaryNodes(const std::vector<sxyz<T1>>& Tx,
                                                    const size_t threadNo) const {

        // clear previously assigned nodes
        tempNodes[threadNo].clear();
        for ( size_t nt=0; nt<tempNeighbors[threadNo].size(); ++nt ) {
            tempNeighbors[threadNo][nt].clear();
        }

        // find cells surrounding Tx
        std::set<T2> txCells;
        for (size_t n=0; n<Tx.size(); ++n) {
            long long i, j, k;
            this->getIJK(Tx[n], i, j, k);

            T2 nsx = dynRadius / this->dx;
            T2 nsy = dynRadius / this->dy;
            T2 nsz = dynRadius / this->dz;

            T1 xstart = this->xmin + (i-nsx-1)*this->dx;
            xstart = xstart < this->xmin ? this->xmin : xstart;
            T1 xstop  = this->xmin + (i+nsx+2)*this->dx;
            xstop = xstop > this->xmax ? this->xmax : xstop;

            T1 ystart = this->ymin + (j-nsy-1)*this->dy;
            ystart = ystart < this->ymin ? this->ymin : ystart;
            T1 ystop  = this->ymin + (j+nsy+2)*this->dy;
            ystop = ystop > this->ymax ? this->ymax : ystop;

            T1 zstart = this->zmin + (k-nsz-1)*this->dz;
            zstart = zstart < this->zmin ? this->zmin : zstart;
            T1 zstop  = this->zmin + (k+nsz+2)*this->dz;
            zstop = zstop > this->zmax ? this->zmax : zstop;

            sxyz<T1> p;
            for ( p.x=xstart+this->dx/2.; p.x<xstop; p.x+=this->dx ) {
                for ( p.y=ystart+this->dy/2.; p.y<ystop; p.y+=this->dy ) {
                    for ( p.z=zstart+this->dz/2.; p.z<zstop; p.z+=this->dz ) {
                        if ( Tx[n].getDistance(p) < dynRadius ) {
                            txCells.insert( this->getCellNo(p) );
                        }
                    }
                }
            }
        }
        if ( verbose )
            std::cout << "\n  *** thread no " << threadNo << ": found " << txCells.size() << " cells within radius ***" << std::endl;

        std::set<T2> adjacentCells(txCells.begin(), txCells.end());

        T2 nTemp = nTertiary * (nSecondary+1);
        
        T1 dxDyn = this->dx / (nTemp + nSecondary + 1);
        T1 dyDyn = this->dy / (nTemp + nSecondary + 1);
        T1 dzDyn = this->dz / (nTemp + nSecondary + 1);

        std::map<std::array<T2,2>,std::vector<T2>> lineMap;
        std::array<T2,2> lineKey;
        typename std::map<std::array<T2,2>,std::vector<T2>>::iterator lineIt;
        
        T2 nnx = this->ncx+1;
        T2 nny = this->ncy+1;

        // edge nodes
        T2 nTmpNodes = 0;
        Node3Dcd<T1,T2> tmpNode;

        sijk<T2> ind;
        for ( auto cell=txCells.begin(); cell!=txCells.end(); cell++ ) {
            this->getCellIJK(*cell, ind);

            if ( ind.i > 0 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j) * this->ncx + ind.i-1);
            if ( ind.i < this->ncx-1 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j) * this->ncx + ind.i+1);
            if ( ind.j > 0 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j-1) * this->ncx + ind.i);
            if ( ind.j < this->ncy-1 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j+1) * this->ncx + ind.i);
            if ( ind.k > 0 )
                adjacentCells.insert( ((ind.k-1) * this->ncy + ind.j) * this->ncx + ind.i);
            if ( ind.k < this->ncz-1 )
                adjacentCells.insert( ((ind.k+1) * this->ncy + ind.j) * this->ncx + ind.i);

            if ( ind.i > 0 && ind.j > 0 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j-1) * this->ncx + ind.i-1);
            if ( ind.i < this->ncx-1 && ind.j > 0 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j-1) * this->ncx + ind.i+1);
            if ( ind.i > 0 && ind.j < this->ncy-1 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j+1) * this->ncx + ind.i-1);
            if ( ind.i < this->ncx-1 && ind.j < this->ncy-1 )
                adjacentCells.insert( (ind.k * this->ncy + ind.j+1) * this->ncx + ind.i+1);

            if ( ind.i > 0 && ind.k > 0 )
                adjacentCells.insert( ((ind.k-1) * this->ncy + ind.j) * this->ncx + ind.i-1);
            if ( ind.i < this->ncx-1 && ind.k > 0 )
                adjacentCells.insert( ((ind.k-1) * this->ncy + ind.j) * this->ncx + ind.i+1);
            if ( ind.i > 0 && ind.k < this->ncz-1 )
                adjacentCells.insert( ((ind.k+1) * this->ncy + ind.j) * this->ncx + ind.i-1);
            if ( ind.i < this->ncx-1 && ind.k < this->ncz-1 )
                adjacentCells.insert( ((ind.k+1) * this->ncy + ind.j) * this->ncx + ind.i+1);

            if ( ind.j > 0 && ind.k > 0 )
                adjacentCells.insert( ((ind.k-1) * this->ncy + ind.j-1) * this->ncx + ind.i);
            if ( ind.j < this->ncy-1 && ind.k > 0 )
                adjacentCells.insert( ((ind.k-1) * this->ncy + ind.j+1) * this->ncx + ind.i);
            if ( ind.j > 0 && ind.k < this->ncz-1 )
                adjacentCells.insert( ((ind.k+1) * this->ncy + ind.j-1) * this->ncx + ind.i);
            if ( ind.j < this->ncy-1 && ind.k < this->ncz-1 )
                adjacentCells.insert( ((ind.k+1) * this->ncy + ind.j+1) * this->ncx + ind.i);

            T1 x0 = this->xmin + ind.i*this->dx;
            T1 y0 = this->ymin + ind.j*this->dy;
            T1 z0 = this->zmin + ind.k*this->dz;

            //
            // along X
            //
            for ( T2 j=0; j<2; ++j ) {
                for ( T2 k=0; k<2; ++k ) {
                    
                    lineKey = { ((ind.k+k)*nny + ind.j+j) * nnx + ind.i,
                                ((ind.k+k)*nny + ind.j+j) * nnx + ind.i+1 };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt == lineMap.end() ) {
                        // not found, insert new pair
                        lineMap[ lineKey ] = std::vector<T2>(nTemp);
                        
                        size_t nd = 0;
                        for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                            for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                                tmpNode.setXYZindex(x0 + (1+n2*(nTertiary+1)+n3)*dxDyn,
                                                    y0 + j*this->dy,
                                                    z0 + k*this->dz,
                                                    nPermanent+nTmpNodes );
                                
                                lineMap[lineKey][nd++] = nTmpNodes++;
                                tempNodes[threadNo].push_back( tmpNode );
                                tempNodes[threadNo].back().pushOwner( *cell );
                            }
                        }
                    } else {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *cell );
                        }
                    }
                }
            }
            
            //
            // along Y
            //
            for ( T2 i=0; i<2; ++i ) {
                for ( T2 k=0; k<2; ++k ) {
                    
                    lineKey = { ((ind.k+k)*nny + ind.j)   * nnx + ind.i+i,
                                ((ind.k+k)*nny + ind.j+1) * nnx + ind.i+i };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt == lineMap.end() ) {
                        // not found, insert new pair
                        lineMap[ lineKey ] = std::vector<T2>(nTemp);
                        
                        size_t nd = 0;
                        for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                            for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                                tmpNode.setXYZindex(x0 + i*this->dx,
                                                    y0 + (1+n2*(nTertiary+1)+n3)*dyDyn,
                                                    z0 + k*this->dz,
                                                    nPermanent+nTmpNodes );
                                
                                lineMap[lineKey][nd++] = nTmpNodes++;
                                tempNodes[threadNo].push_back( tmpNode );
                                tempNodes[threadNo].back().pushOwner( *cell );
                            }
                        }
                    } else {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *cell );
                        }
                    }
                }
            }

            //
            // along Z
            //
            for ( T2 i=0; i<2; ++i ) {
                for ( T2 j=0; j<2; ++j ) {
                    
                    lineKey = { ((ind.k)  *nny + ind.j+j) * nnx + ind.i+i,
                                ((ind.k+1)*nny + ind.j+j) * nnx + ind.i+i };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt == lineMap.end() ) {
                        // not found, insert new pair
                        lineMap[ lineKey ] = std::vector<T2>(nTemp);
                        
                        size_t nd = 0;
                        for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                            for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                                tmpNode.setXYZindex(x0 + i*this->dx,
                                                    y0 + j*this->dy,
                                                    z0 + (1+n2*(nTertiary+1)+n3)*dzDyn,
                                                    nPermanent+nTmpNodes );
                                
                                lineMap[lineKey][nd++] = nTmpNodes++;
                                tempNodes[threadNo].push_back( tmpNode );
                                tempNodes[threadNo].back().pushOwner( *cell );
                            }
                        }
                    } else {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *cell );
                        }
                    }
                }
            }
        }
        
        std::map<std::array<T2,4>,std::vector<T2>> faceMap;
        std::array<T2,4> faceKey;
        typename std::map<std::array<T2,4>,std::vector<T2>>::iterator faceIt;
        nTemp = (nTertiary * (nSecondary+1) + nSecondary) * (nTertiary * (nSecondary+1) + nSecondary) - nSecondary*nSecondary;
        
        for ( auto cell=txCells.begin(); cell!=txCells.end(); cell++ ) {
            this->getCellIJK(*cell, ind);

            //
            // XY faces
            //
            for ( T2 k=0; k<2; ++k ) {
                faceKey = { ((ind.k+k)*nny + ind.j) * nnx + ind.i,
                    ((ind.k+k)*nny + ind.j) * nnx + ind.i+1,
                    ((ind.k+k)*nny + ind.j+1) * nnx + ind.i,
                    ((ind.k+k)*nny + ind.j+1) * nnx + ind.i+1 };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt == faceMap.end() ) {
                    // not found, insert new pair
                    faceMap[ faceKey ] = std::vector<T2>(nTemp);
                } else {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *cell );
                    }
                    continue;
                }

                T1 x0 = this->xmin + ind.i*this->dx;
                T1 y0 = this->ymin + ind.j*this->dy;
                T1 z0 = this->zmin + ind.k+k*this->dz;

                size_t ifn = 0;
                size_t n0 = 0;
                while (n0 < nTertiary*(nSecondary+1)+nSecondary) {
                    for ( size_t n1=0; n1<nTertiary; ++n1 ) {
                        y0 += dyDyn;
                        for ( size_t n2=0; n2<nTertiary*(nSecondary+1)+nSecondary; ++n2 ) {
                            tmpNode.setXYZindex(x0 + (n2+1)*dxDyn,
                                                y0,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                        n0++;
                    }
                    if (n0 == nTertiary*(nSecondary+1)+nSecondary) {
                        break;
                    }
                    y0 += dyDyn;
                    for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                        for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                            tmpNode.setXYZindex(x0 + (1+n2*(nTertiary+1)+n3)*dxDyn,
                                                y0,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                    }
                    n0++;
                }
            }
            
            //
            // XZ faces
            //
            for ( T2 j=0; j<2; ++j ) {
                faceKey = { ((ind.k)*nny + ind.j+j) * nnx + ind.i,
                    ((ind.k)*nny + ind.j+j) * nnx + ind.i+1,
                    ((ind.k+1)*nny + ind.j+j) * nnx + ind.i,
                    ((ind.k+1)*nny + ind.j+j) * nnx + ind.i+1 };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt == faceMap.end() ) {
                    // not found, insert new pair
                    faceMap[ faceKey ] = std::vector<T2>(nTemp);
                } else {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *cell );
                    }
                    continue;
                }
                
                T1 x0 = this->xmin + ind.i*this->dx;
                T1 y0 = this->ymin + ind.j+j*this->dy;
                T1 z0 = this->zmin + ind.k*this->dz;
                
                size_t ifn = 0;
                size_t n0 = 0;
                while (n0 < nTertiary*(nSecondary+1)+nSecondary) {
                    for ( size_t n1=0; n1<nTertiary; ++n1 ) {
                        z0 += dzDyn;
                        for ( size_t n2=0; n2<nTertiary*(nSecondary+1)+nSecondary; ++n2 ) {
                            tmpNode.setXYZindex(x0 + (n2+1)*dxDyn,
                                                y0,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                        n0++;
                    }
                    if (n0 == nTertiary*(nSecondary+1)+nSecondary) {
                        break;
                    }
                    z0 += dzDyn;
                    for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                        for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                            tmpNode.setXYZindex(x0 + (1+n2*(nTertiary+1)+n3)*dxDyn,
                                                y0,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                    }
                    n0++;
                }
            }
            
            //
            // YZ faces
            //
            for ( T2 i=0; i<2; ++i ) {
                faceKey = { ((ind.k)*nny + ind.j) * nnx + ind.i+i,
                    ((ind.k)*nny + ind.j+1) * nnx + ind.i+i,
                    ((ind.k+1)*nny + ind.j) * nnx + ind.i+i,
                    ((ind.k+1)*nny + ind.j+1) * nnx + ind.i+i };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt == faceMap.end() ) {
                    // not found, insert new pair
                    faceMap[ faceKey ] = std::vector<T2>(nTemp);
                } else {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *cell );
                    }
                    continue;
                }
                
                T1 x0 = this->xmin + ind.i+i*this->dx;
                T1 y0 = this->ymin + ind.j*this->dy;
                T1 z0 = this->zmin + ind.k*this->dz;
                
                size_t ifn = 0;
                size_t n0 = 0;
                while (n0 < nTertiary*(nSecondary+1)+nSecondary) {
                    for ( size_t n1=0; n1<nTertiary; ++n1 ) {
                        z0 += dzDyn;
                        for ( size_t n2=0; n2<nTertiary*(nSecondary+1)+nSecondary; ++n2 ) {
                            tmpNode.setXYZindex(x0,
                                                y0 + (n2+1)*dyDyn,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                        n0++;
                    }
                    if (n0 == nTertiary*(nSecondary+1)+nSecondary) {
                        break;
                    }
                    z0 += dzDyn;
                    for ( size_t n2=0; n2<nSecondary+1; ++n2 ) {
                        for ( size_t n3=0; n3<nTertiary; ++n3 ) {
                            tmpNode.setXYZindex(x0,
                                                y0 + (1+n2*(nTertiary+1)+n3)*dyDyn,
                                                z0,
                                                nPermanent+nTmpNodes );
                            
                            faceMap[faceKey][ifn++] = nTmpNodes++;
                            tempNodes[threadNo].push_back( tmpNode );
                            tempNodes[threadNo].back().pushOwner( *cell );
                        }
                    }
                    n0++;
                }
            }
        }
        
        for ( auto cell=txCells.begin(); cell!=txCells.end(); ++cell ) {
            adjacentCells.erase(*cell);
        }
        for ( auto adj=adjacentCells.begin(); adj!=adjacentCells.end(); ++adj ) {
            this->getCellIJK(*adj, ind);
            
            //
            // along X
            //
            for ( T2 j=0; j<2; ++j ) {
                for ( T2 k=0; k<2; ++k ) {
                    
                    lineKey = { ((ind.k+k)*nny + ind.j+j) * nnx + ind.i,
                        ((ind.k+k)*nny + ind.j+j) * nnx + ind.i+1 };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt != lineMap.end() ) {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *adj );
                        }
                    }
                }
            }
            
            //
            // along Y
            //
            for ( T2 i=0; i<2; ++i ) {
                for ( T2 k=0; k<2; ++k ) {
                    
                    lineKey = { ((ind.k+k)*nny + ind.j)   * nnx + ind.i+i,
                        ((ind.k+k)*nny + ind.j+1) * nnx + ind.i+i };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt != lineMap.end() ) {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *adj );
                        }
                    }
                }
            }
            
            //
            // along Z
            //
            for ( T2 i=0; i<2; ++i ) {
                for ( T2 j=0; j<2; ++j ) {
                    
                    lineKey = { ((ind.k)  *nny + ind.j+j) * nnx + ind.i+i,
                        ((ind.k+1)*nny + ind.j+j) * nnx + ind.i+i };
                    std::sort(lineKey.begin(), lineKey.end());
                    
                    lineIt = lineMap.find( lineKey );
                    if ( lineIt != lineMap.end() ) {
                        for ( size_t n=0; n<lineIt->second.size(); ++n ) {
                            // setting owners
                            tempNodes[threadNo][ lineIt->second[n] ].pushOwner( *adj );
                        }
                    }
                }
            }
            
            //
            // XY faces
            //
            for ( T2 k=0; k<2; ++k ) {
                faceKey = { ((ind.k+k)*nny + ind.j) * nnx + ind.i,
                    ((ind.k+k)*nny + ind.j) * nnx + ind.i+1,
                    ((ind.k+k)*nny + ind.j+1) * nnx + ind.i,
                    ((ind.k+k)*nny + ind.j+1) * nnx + ind.i+1 };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt != faceMap.end() ) {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *adj );
                    }
                }
            }
            
            //
            // XZ faces
            //
            for ( T2 j=0; j<2; ++j ) {
                faceKey = { ((ind.k)*nny + ind.j+j) * nnx + ind.i,
                    ((ind.k)*nny + ind.j+j) * nnx + ind.i+1,
                    ((ind.k+1)*nny + ind.j+j) * nnx + ind.i,
                    ((ind.k+1)*nny + ind.j+j) * nnx + ind.i+1 };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt != faceMap.end() ) {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *adj );
                    }
                }
            }
            
            //
            // YZ faces
            //
            for ( T2 i=0; i<2; ++i ) {
                faceKey = { ((ind.k)*nny + ind.j) * nnx + ind.i+i,
                    ((ind.k)*nny + ind.j+1) * nnx + ind.i+i,
                    ((ind.k+1)*nny + ind.j) * nnx + ind.i+i,
                    ((ind.k+1)*nny + ind.j+1) * nnx + ind.i+i };
                std::sort(faceKey.begin(), faceKey.end());
                
                faceIt = faceMap.find( faceKey );
                if ( faceIt != faceMap.end() ) {
                    for ( size_t n=0; n<faceIt->second.size(); ++n ) {
                        // setting owners
                        tempNodes[threadNo][ faceIt->second[n] ].pushOwner( *adj );
                    }
                }
            }
        }
        
        for ( T2 n=0; n<tempNodes[threadNo].size(); ++n ) {
            for ( size_t n2=0; n2<tempNodes[threadNo][n].getOwners().size(); ++n2) {
                tempNeighbors[threadNo][ tempNodes[threadNo][n].getOwners()[n2] ].push_back(n);
            }
        }
        if ( verbose )
            std::cout << "  *** thread no " << threadNo << ": " << tempNodes[threadNo].size() << " dynamic nodes were added ***" << std::endl;

//#ifdef VTK
//        vtkSmartPointer<vtkPolyData> polydata = vtkSmartPointer<vtkPolyData>::New();
//        vtkSmartPointer<vtkPoints> pts = vtkSmartPointer<vtkPoints>::New();
//        for ( size_t n=0; n<tempNodes[threadNo].size(); ++n ) {
//            pts->InsertNextPoint(tempNodes[threadNo][n].getX(),
//                                 tempNodes[threadNo][n].getY(),
//                                 tempNodes[threadNo][n].getZ());
//        }
//        polydata->SetPoints(pts);
//
//        vtkSmartPointer<vtkXMLPolyDataWriter> writer = vtkSmartPointer<vtkXMLPolyDataWriter>::New();
//        writer->SetFileName( "tempNodes.vtk" );
//        writer->SetInputData( polydata );
//        writer->SetDataModeToBinary();
//        writer->Update();
//#endif

    }
    
    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                           const std::vector<T1>& t0,
                                           const std::vector<sxyz<T1>>& Rx,
                                           const size_t threadNo) const {
        this->checkPts(Tx);
        this->checkPts(Rx);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> queue( cmp );
        
        addTemporaryNodes(Tx, threadNo);
        
        std::vector<Node3Dcd<T1,T2>> txNodes;
        std::vector<bool> inQueue( this->nodes.size()+tempNodes[threadNo].size(), false );
        std::vector<bool> frozen( this->nodes.size()+tempNodes[threadNo].size(), false );
        
        initQueue(Tx, t0, queue, txNodes, inQueue, frozen, threadNo);
        
        propagate(queue, inQueue, frozen, threadNo);
    }
    
    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                           const std::vector<T1>& t0,
                                           const std::vector<const std::vector<sxyz<T1>>*>& Rx,
                                           const size_t threadNo) const {
        this->checkPts(Tx);
        for ( size_t n=0; n<Rx.size(); ++n )
            this->checkPts(*Rx[n]);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> queue( cmp );
        
        addTemporaryNodes(Tx, threadNo);
        
        std::vector<Node3Dcd<T1,T2>> txNodes;
        std::vector<bool> inQueue( this->nodes.size()+tempNodes[threadNo].size(), false );
        std::vector<bool> frozen( this->nodes.size()+tempNodes[threadNo].size(), false );
        
        initQueue(Tx, t0, queue, txNodes, inQueue, frozen, threadNo);
        
        propagate(queue, inQueue, frozen, threadNo);
    }


    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::initQueue(const std::vector<sxyz<T1>>& Tx,
                                            const std::vector<T1>& t0,
                                            std::priority_queue<Node3Dc<T1,T2>*,
                                            std::vector<Node3Dc<T1,T2>*>,
                                            CompareNodePtr<T1>>& queue,
                                            std::vector<Node3Dcd<T1,T2>>& txNodes,
                                            std::vector<bool>& inQueue,
                                            std::vector<bool>& frozen,
                                            const size_t threadNo) const {
        
        for (size_t n=0; n<Tx.size(); ++n) {
            bool found = false;
            for ( size_t nn=0; nn<this->nodes.size(); ++nn ) {
                if ( this->nodes[nn] == Tx[n] ) {
                    found = true;
                    this->nodes[nn].setTT( t0[n], threadNo );
                    queue.push( &(this->nodes[nn]) );
                    inQueue[nn] = true;
                    frozen[nn] = true;
                    break;
                }
            }
            if ( found==false ) {
                for ( size_t nn=0; nn<tempNodes[threadNo].size(); ++nn ) {
                    if ( tempNodes[threadNo][nn] == Tx[n] ) {
                        found = true;
                        tempNodes[threadNo][nn].setTT( t0[n], 0 );
                        queue.push( &(tempNodes[threadNo][nn]) );
                        inQueue[nPermanent+nn] = true;
                        frozen[nPermanent+nn] = true;
                        break;
                    }
                }
            }
            if ( found==false ) {
                // If Tx[n] is not on a node, we create a new node and initialize the queue:
                txNodes.push_back( Node3Dcd<T1,T2>(t0[n], Tx[n].x, Tx[n].y, Tx[n].z, 1, 0));
                txNodes.back().pushOwner( this->getCellNo(Tx[n]) );
                txNodes.back().setGridIndex( static_cast<T2>(this->nodes.size()+
                                                             tempNodes.size()+
                                                             txNodes.size()-1) );
                frozen.push_back( true );
                
                queue.push( &(txNodes.back()) );
                inQueue.push_back( true );
                
            }
        }
    }
    
    template<typename T1, typename T2, typename CELL>
    void Grid3Drcdsp<T1,T2,CELL>::propagate(std::priority_queue<Node3Dc<T1,T2>*,
                                            std::vector<Node3Dc<T1,T2>*>,
                                            CompareNodePtr<T1>>& queue,
                                            std::vector<bool>& inQueue,
                                            std::vector<bool>& frozen,
                                            const size_t threadNo) const {
        
        while ( !queue.empty() ) {
            const Node3Dc<T1,T2>* src = queue.top();
            queue.pop();
            inQueue[ src->getGridIndex() ] = false;
            frozen[ src->getGridIndex() ] = true;
            
            T1 srcTT;
            if ( src->getGridIndex() >= nPermanent )
                srcTT = src->getTT(0);
            else
                srcTT = src->getTT(threadNo);
            
            for ( size_t no=0; no<src->getOwners().size(); ++no ) {
                
                T2 cellNo = src->getOwners()[no];
                
                for ( size_t k=0; k< this->neighbors[cellNo].size(); ++k ) {
                    T2 neibNo = this->neighbors[cellNo][k];
                    if ( neibNo == src->getGridIndex() || frozen[neibNo] ) {
                        continue;
                    }
                    
                    // compute dt
                    T1 dt = this->cells.computeDt(*src, this->nodes[neibNo], cellNo);
                    
                    if (srcTT+dt < this->nodes[neibNo].getTT(threadNo)) {
                        this->nodes[neibNo].setTT( srcTT+dt, threadNo );
                        
                        if ( !inQueue[neibNo] ) {
                            queue.push( &(this->nodes[neibNo]) );
                            inQueue[neibNo] = true;
                        }
                    }
                }
                
                for ( size_t k=0; k < tempNeighbors[threadNo][cellNo].size(); ++k ) {
                    T2 neibNo = tempNeighbors[threadNo][cellNo][k];
                    if ( neibNo == src->getGridIndex()-nPermanent || frozen[nPermanent+neibNo] ) {
                        continue;
                    }
                    
                    // compute dt
                    T1 dt = this->cells.computeDt(*src, tempNodes[threadNo][neibNo], cellNo);
                    if (srcTT+dt < tempNodes[threadNo][neibNo].getTT(0)) {
                        tempNodes[threadNo][neibNo].setTT(srcTT+dt,0);
                        
                        if ( !inQueue[nPermanent+neibNo] ) {
                            queue.push( &(tempNodes[threadNo][neibNo]) );
                            inQueue[nPermanent+neibNo] = true;
                        }
                    }
                }
            }
        }
    }

}
#endif /* Grid3Drcdsp_h */
