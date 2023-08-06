//
//  Grid3Ducfm.h
//  ttcr
//
//  Created by Bernard Giroux on 2014-02-13.
//  Copyright (c) 2014 Bernard Giroux. All rights reserved.
//

/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

//  Reference paper for local solver
//
//@ARTICLE{qian07,
//	author = {Qian, Jianliang and Zhang, Yong-Tao and Zhao, Hong-Kai},
//	title = {Fast Sweeping Methods for Eikonal Equations on Triangular Meshes},
//	journal = {SIAM Journal on Numerical Analysis},
//	year = {2007},
//	volume = {45},
//	pages = {83--107},
//	number = {1},
//	month = jan,
//	doi = {10.1137/050627083},
//	issn = {00361429},
//	owner = {giroux},
//	publisher = {Society for Industrial and Applied Mathematics},
//	timestamp = {2014.01.26},
//	url = {http://www.jstor.org/stable/40232919}
//	}
//

#ifndef ttcr_Grid3Ducfm_h
#define ttcr_Grid3Ducfm_h

#include <cmath>
#include <fstream>
#include <queue>
#include <vector>

#include "Grid3Duc.h"
#include "Node3Dc.h"

namespace ttcr {
    
    template<typename T1, typename T2>
    class Grid3Ducfm : public Grid3Duc<T1,T2,Node3Dc<T1,T2>> {
    public:
        Grid3Ducfm(const std::vector<sxyz<T1>>& no,
                   const std::vector<tetrahedronElem<T2>>& tet,
                   const bool rp, const bool rptt, const T1 md,
                   const size_t nt=1) :
        Grid3Duc<T1,T2,Node3Dc<T1,T2>>(no, tet, rp, rptt, md, nt)
        {
            this->buildGridNodes(no, nt);
            this->template buildGridNeighbors<Node3Dc<T1,T2>>(this->nodes);
        }
        
        ~Grid3Ducfm() {
        }
        
        void raytrace(const std::vector<sxyz<T1>>& Tx,
                     const std::vector<T1>& t0,
                     const std::vector<sxyz<T1>>& Rx,
                     std::vector<T1>& traveltimes,
                     const size_t threadNo=0) const;
        
        void raytrace(const std::vector<sxyz<T1>>&,
                     const std::vector<T1>&,
                     const std::vector<const std::vector<sxyz<T1>>*>&,
                     std::vector<std::vector<T1>*>&,
                     const size_t=0) const;
        
        void raytrace(const std::vector<sxyz<T1>>&,
                     const std::vector<T1>& ,
                     const std::vector<sxyz<T1>>&,
                     std::vector<T1>&,
                     std::vector<std::vector<sxyz<T1>>>&,
                     const size_t=0) const;
        
        void raytrace(const std::vector<sxyz<T1>>&,
                     const std::vector<T1>&,
                     const std::vector<const std::vector<sxyz<T1>>*>&,
                     std::vector<std::vector<T1>*>&,
                     std::vector<std::vector<std::vector<sxyz<T1>>>*>&,
                     const size_t=0) const;
        
    private:
        
        void initBand(const std::vector<sxyz<T1>>& Tx,
                      const std::vector<T1>& t0,
                      std::priority_queue<Node3Dc<T1,T2>*,
                      std::vector<Node3Dc<T1,T2>*>,
                      CompareNodePtr<T1>>&,
                      std::vector<bool>&,
                      std::vector<bool>&,
                      const size_t) const;
        
        void propagate(std::priority_queue<Node3Dc<T1,T2>*,
                       std::vector<Node3Dc<T1,T2>*>,
                       CompareNodePtr<T1>>&,
                       std::vector<bool>&,
                       std::vector<bool>&,
                       const size_t) const;
        
    };
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                     const std::vector<T1>& t0,
                                     const std::vector<sxyz<T1>>& Rx,
                                     std::vector<T1>& traveltimes,
                                     const size_t threadNo) const {
        
        this->checkPts(Tx);
        this->checkPts(Rx);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> narrow_band( cmp );
        
        std::vector<bool> inQueue( this->nodes.size(), false );
        std::vector<bool> frozen( this->nodes.size(), false );
        
        initBand(Tx, t0, narrow_band, inQueue, frozen, threadNo);
        
        propagate(narrow_band, inQueue, frozen, threadNo);
        
        if ( traveltimes.size() != Rx.size() ) {
            traveltimes.resize( Rx.size() );
        }
        
        if ( this->tt_from_rp ) {
            for (size_t n=0; n<Rx.size(); ++n) {
                traveltimes[n] = this->getTraveltimeFromRaypath(Tx, t0, Rx[n], threadNo);
            }
        } else {
            for (size_t n=0; n<Rx.size(); ++n) {
                traveltimes[n] = this->getTraveltime(Rx[n], this->nodes, threadNo);
            }
        }
    }
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                     const std::vector<T1>& t0,
                                     const std::vector<const std::vector<sxyz<T1>>*>& Rx,
                                     std::vector<std::vector<T1>*>& traveltimes,
                                     const size_t threadNo) const {
        
        this->checkPts(Tx);
        for ( size_t n=0; n<Rx.size(); ++n )
            this->checkPts(*Rx[n]);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> narrow_band( cmp );
        
        std::vector<bool> inBand( this->nodes.size(), false );
        std::vector<bool> frozen( this->nodes.size(), false );
        
        initBand(Tx, t0, narrow_band, inBand, frozen, threadNo);
        
        propagate(narrow_band, inBand, frozen, threadNo);
        
        if ( traveltimes.size() != Rx.size() ) {
            traveltimes.resize( Rx.size() );
        }
        
        if ( this->tt_from_rp ) {
            for (size_t nr=0; nr<Rx.size(); ++nr) {
                traveltimes[nr]->resize( Rx[nr]->size() );
                for (size_t n=0; n<Rx[nr]->size(); ++n)
                    (*traveltimes[nr])[n] = this->getTraveltimeFromRaypath(Tx, t0, (*Rx[nr])[n], threadNo);
            }
        } else {
            for (size_t nr=0; nr<Rx.size(); ++nr) {
                traveltimes[nr]->resize( Rx[nr]->size() );
                for (size_t n=0; n<Rx[nr]->size(); ++n)
                    (*traveltimes[nr])[n] = this->getTraveltime((*Rx[nr])[n], this->nodes, threadNo);
            }
        }
    }
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                     const std::vector<T1>& t0,
                                     const std::vector<sxyz<T1>>& Rx,
                                     std::vector<T1>& traveltimes,
                                     std::vector<std::vector<sxyz<T1>>>& r_data,
                                     const size_t threadNo) const {
        
        this->checkPts(Tx);
        this->checkPts(Rx);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> narrow_band( cmp );
        
        std::vector<bool> inQueue( this->nodes.size(), false );
        std::vector<bool> frozen( this->nodes.size(), false );
        
        initBand(Tx, t0, narrow_band, inQueue, frozen, threadNo);
        
        propagate(narrow_band, inQueue, frozen, threadNo);
        
        if ( traveltimes.size() != Rx.size() ) {
            traveltimes.resize( Rx.size() );
        }
        if ( r_data.size() != Rx.size() ) {
            r_data.resize( Rx.size() );
        }
        for ( size_t ni=0; ni<r_data.size(); ++ni ) {
            r_data[ni].resize( 0 );
        }
        
        for (size_t n=0; n<Rx.size(); ++n) {
            this->getRaypath(Tx, t0, Rx[n], r_data[n], traveltimes[n], threadNo);
        }
    }
    
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::raytrace(const std::vector<sxyz<T1>>& Tx,
                                     const std::vector<T1>& t0,
                                     const std::vector<const std::vector<sxyz<T1>>*>& Rx,
                                     std::vector<std::vector<T1>*>& traveltimes,
                                     std::vector<std::vector<std::vector<sxyz<T1>>>*>& r_data,
                                     const size_t threadNo) const {
        
        this->checkPts(Tx);
        for ( size_t n=0; n<Rx.size(); ++n )
            this->checkPts(*Rx[n]);
        
        for ( size_t n=0; n<this->nodes.size(); ++n ) {
            this->nodes[n].reinit( threadNo );
        }
        
        CompareNodePtr<T1> cmp(threadNo);
        std::priority_queue< Node3Dc<T1,T2>*, std::vector<Node3Dc<T1,T2>*>,
        CompareNodePtr<T1>> narrow_band( cmp );
        
        std::vector<bool> inBand( this->nodes.size(), false );
        std::vector<bool> frozen( this->nodes.size(), false );
        
        initBand(Tx, t0, narrow_band, inBand, frozen, threadNo);
        
        propagate(narrow_band, inBand, frozen, threadNo);
        
        if ( traveltimes.size() != Rx.size() ) {
            traveltimes.resize( Rx.size() );
        }
        if ( r_data.size() != Rx.size() ) {
            r_data.resize( Rx.size() );
        }
        
        for (size_t nr=0; nr<Rx.size(); ++nr) {
            traveltimes[nr]->resize( Rx[nr]->size() );
            r_data[nr]->resize( Rx[nr]->size() );
            for ( size_t ni=0; ni<r_data[nr]->size(); ++ni ) {
                (*r_data[nr])[ni].resize( 0 );
            }
            
            for (size_t n=0; n<Rx[nr]->size(); ++n) {
                this->getRaypath(Tx, t0, (*Rx[nr])[n], (*r_data[nr])[n],
                                 (*traveltimes[nr])[n], threadNo);
            }
        }
    }
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::initBand(const std::vector<sxyz<T1>>& Tx,
                                     const std::vector<T1>& t0,
                                     std::priority_queue<Node3Dc<T1,T2>*,
                                     std::vector<Node3Dc<T1,T2>*>,
                                     CompareNodePtr<T1>>& narrow_band,
                                     std::vector<bool>& inBand,
                                     std::vector<bool>& frozen,
                                     const size_t threadNo) const {
        
        for (size_t n=0; n<Tx.size(); ++n) {
            bool found = false;
            for ( size_t nn=0; nn<this->nodes.size(); ++nn ) {
                if ( this->nodes[nn] == Tx[n] ) {
                    found = true;
                    this->nodes[nn].setTT( t0[n], threadNo );
                    narrow_band.push( &(this->nodes[nn]) );
                    inBand[nn] = true;
                    frozen[nn] = true;
                    
                    if ( Tx.size()==1 ) {
                        if ( Grid3Duc<T1,T2,Node3Dc<T1,T2>>::source_radius == 0.0 ) {
                            // populate around Tx
                            for ( size_t no=0; no<this->nodes[nn].getOwners().size(); ++no ) {
                                
                                T2 cellNo = this->nodes[nn].getOwners()[no];
                                for ( size_t k=0; k< this->neighbors[cellNo].size(); ++k ) {
                                    T2 neibNo = this->neighbors[cellNo][k];
                                    if ( neibNo == nn ) continue;
                                    T1 dt = this->computeDt(this->nodes[nn], this->nodes[neibNo], cellNo);
                                    
                                    if ( t0[n]+dt < this->nodes[neibNo].getTT(threadNo) ) {
                                        this->nodes[neibNo].setTT( t0[n]+dt, threadNo );
                                        
                                        if ( !inBand[neibNo] ) {
                                            narrow_band.push( &(this->nodes[neibNo]) );
                                            inBand[neibNo] = true;
                                            frozen[neibNo] = true;
                                        }
                                    }
                                }
                            }
                        } else {
                            
                            // find nodes within source radius
                            size_t nodes_added = 0;
                            for ( size_t no=0; no<this->nodes.size(); ++no ) {
                                
                                if ( no == nn ) continue;
                                
                                T1 d = this->nodes[nn].getDistance( this->nodes[no] );
                                if ( d <= Grid3Duc<T1,T2,Node3Dc<T1,T2>>::source_radius ) {
                                    
                                    // compute average slowness with cells touching the source node
                                    T1 slown = 0.0;
                                    for ( size_t nc=0; nc<this->nodes[nn].getOwners().size(); ++nc ) {
                                        slown += Grid3Duc<T1,T2,Node3Dc<T1,T2>>::slowness[this->nodes[nn].getOwners()[nc]];
                                    }
                                    slown /= this->nodes[nn].getOwners().size();
                                    T1 dt = d * slown;
                                    
                                    if ( t0[n]+dt < this->nodes[no].getTT(threadNo) ) {
                                        this->nodes[no].setTT( t0[n]+dt, threadNo );
                                        
                                        if ( !inBand[no] ) {
                                            narrow_band.push( &(this->nodes[no]) );
                                            inBand[no] = true;
                                            frozen[no] = true;
                                            nodes_added++;
                                        }
                                    }
                                }
                            }
                            if ( nodes_added == 0 ) {
                                std::cerr << "Error: no nodes found within source radius, aborting" << std::endl;
                                abort();
                            } else {
                                std::cout << "(found " << nodes_added << " nodes around Tx point)\n";
                            }
                        }
                    }
                    
                    break;
                }
            }
            if ( found==false ) {
                
                T2 cellNo = this->getCellNo(Tx[n]);
                if ( Grid3Duc<T1,T2,Node3Dc<T1,T2>>::source_radius == 0.0 ) {
                    // populate around Tx
                    
                    for ( size_t k=0; k< this->neighbors[cellNo].size(); ++k ) {
                        T2 neibNo = this->neighbors[cellNo][k];
                        
                        // compute dt
                        T1 dt = this->computeDt(this->nodes[neibNo], Tx[n], cellNo);
                        
                        this->nodes[neibNo].setTT( t0[n]+dt, threadNo );
                        narrow_band.push( &(this->nodes[neibNo]) );
                        inBand[neibNo] = true;
                        frozen[neibNo] = true;
                    }
                } else if ( Tx.size()==1 ) { // look into source radius only for point sources
                    
                    // find nodes within source radius
                    size_t nodes_added = 0;
                    for ( size_t no=0; no<this->nodes.size(); ++no ) {
                        
                        T1 d = this->nodes[no].getDistance( Tx[n] );
                        if ( d <= Grid3Duc<T1,T2,Node3Dc<T1,T2>>::source_radius ) {
                            
                            T1 dt = d * Grid3Duc<T1,T2,Node3Dc<T1,T2>>::slowness[cellNo];
                            
                            if ( t0[n]+dt < this->nodes[no].getTT(threadNo) ) {
                                this->nodes[no].setTT( t0[n]+dt, threadNo );
                                
                                if ( !inBand[no] ) {
                                    narrow_band.push( &(this->nodes[no]) );
                                    inBand[no] = true;
                                    frozen[no] = true;
                                    nodes_added++;
                                }
                            }
                        }
                    }
                    if ( nodes_added == 0 ) {
                        std::cerr << "Error: no nodes found within source radius, aborting" << std::endl;
                        abort();
                    } else {
                        std::cout << "(found " << nodes_added << " nodes around Tx point)\n";
                    }
                }
            }
        }
    }
    
    template<typename T1, typename T2>
    void Grid3Ducfm<T1,T2>::propagate(std::priority_queue<Node3Dc<T1,T2>*,
                                      std::vector<Node3Dc<T1,T2>*>,
                                      CompareNodePtr<T1>>& narrow_band,
                                      std::vector<bool>& inNarrowBand,
                                      std::vector<bool>& frozen,
                                      const size_t threadNo) const {
        
        while ( !narrow_band.empty() ) {
            
            const Node3Dc<T1,T2>* source = narrow_band.top();
            narrow_band.pop();
            inNarrowBand[ source->getGridIndex() ] = false;
            frozen[ source->getGridIndex() ] = true;   // marked as known
            
            for ( size_t no=0; no<source->getOwners().size(); ++no ) {
                
                T2 cellNo = source->getOwners()[no];
                
                for ( size_t k=0; k< this->neighbors[cellNo].size(); ++k ) {
                    T2 neibNo = this->neighbors[cellNo][k];
                    if ( neibNo == source->getGridIndex() || frozen[neibNo] ) {
                        continue;
                    }
                    
                    //				this->local3Dsolver( &(this->nodes[neibNo]), threadNo );
                    this->localUpdate3D( &(this->nodes[neibNo]), threadNo );
                    
                    if ( !inNarrowBand[neibNo] ) {
                        narrow_band.push( &(this->nodes[neibNo]) );
                        inNarrowBand[neibNo] = true;
                    }
                }
            }
        }
    }
    
}

#endif
